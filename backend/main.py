import logging.config
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from api.v1.api import api_router
from fastapi.staticfiles import StaticFiles
from app.shared.shared import frames_queue
import os
from asyncio import CancelledError
import json
import asyncio


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
        while connection_open:  # Use the flag to check connection status
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
        connection_open = False  # Update the flag upon disconnection
        logging.info("WebSocket client disconnected")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        heartbeat_task.cancel()  # Cancel the heartbeat task
        try:
            await websocket.close()
            logging.info("WebSocket connection gracefully closed")
        except Exception as e:
            logging.error(f"Error during WebSocket closure: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
