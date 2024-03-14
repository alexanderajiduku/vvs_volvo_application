import logging.config
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from app.database.database import get_db
from api.v1.api import api_router
from fastapi.staticfiles import StaticFiles
import asyncio
from app.services.vehicle_measure import VehicleDetectionService
from app.shared.shared import frames_queue
import os
from asyncio import CancelledError


def create_application() -> FastAPI:
    app = FastAPI()

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
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
    try:
        while True:
            try:
                height = await frames_queue.get()
                await websocket.send_text(f"{height}")
            except CancelledError:
                logging.info("WebSocket task cancelled, exiting")
                break
    except WebSocketDisconnect:
        logging.info("WebSocket client disconnected")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        await websocket.close()
        logging.info("WebSocket connection closed")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
