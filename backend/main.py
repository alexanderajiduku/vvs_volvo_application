import logging.config
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from fastapi.middleware.cors import CORSMiddleware  
from api.v1.api import api_router
from fastapi.staticfiles import StaticFiles
from app.shared.shared import frames_queue
from asyncio import CancelledError
import json
import asyncio
#from app.services.camera_handler import CameraHandler
import cv2


def create_application() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], 
        allow_credentials=True,
        allow_methods=["*"],  
        allow_headers=["*"],  
    )

    app.include_router(api_router, prefix="/api/v1")
    
    UPLOAD_DIR = "annotated_results"
    app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

    return app



app = create_application()


@app.get("/")
async def home():
    return {"message": "Welcome to the home page!"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logging.info("WebSocket client connected")
    connection_open = True 

    async def heartbeat():
        while connection_open:  
            try:
                await websocket.send_text(json.dumps({"type": "heartbeat"}))
                await asyncio.sleep(10) 
            except Exception as e:
                logging.error(f"Heartbeat failed: {e}")
                break

    heartbeat_task = asyncio.create_task(heartbeat())

    try:
        while connection_open:  
            try:
                height = await frames_queue.get()
                height_json = json.dumps({"height": height})
                await websocket.send_text(height_json)
            except Exception as e:
                logging.error(f"Error sending message: {e}")
            except CancelledError:
                logging.info("WebSocket task cancelled, exiting")
                break
    except WebSocketDisconnect:
        connection_open = False  
        logging.info("WebSocket client disconnected")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        heartbeat_task.cancel()  
        try:
            await websocket.close()
            logging.info("WebSocket connection gracefully closed")
        except Exception as e:
            logging.error(f"Error during WebSocket closure: {e}")

"""

@app.websocket("/ws/video")
async def websocket_video(websocket: WebSocket):
    await websocket.accept()
    camera_handler = CameraHandler()
    camera_handler.start_camera()

    try:
        while True:
            frame = camera_handler.get_frame()
            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                await websocket.send_bytes(buffer.tobytes())
            else:
                break  
            await asyncio.sleep(0.03)  
    except WebSocketDisconnect:
        print("Client disconnected from video stream")
    finally:
        camera_handler.stop_camera() 
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
