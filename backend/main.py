import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.v1.api import api_router
import socketio
from app.database.database import engine, SessionLocal
from app.models.videos import VideoModel
from app.services.vehicle_measure import VehicleDetectionService
from app.core.cors import setup_cors

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

UPLOAD_DIR = "truckmeasure_uploads"

try:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
except OSError as e:
    logger.error(f"Error creating directory: {e}")

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

setup_cors(app)

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')  
socket_app = socketio.ASGIApp(sio, app)


@sio.event
async def start_vehicle_detection(sid, data):
    input_source = data.get('input_source')
    model_id = data.get('model_id')  
    if not model_id:
        await sio.emit('error', {'message': 'model_id is missing'}, to=sid)
        return

    db_session = SessionLocal() 
    try:
        detection_service = VehicleDetectionService(model_id=model_id, db_session=db_session)  
        await detection_service.process_video_with_socketio(input_source, sio, sid)
    finally:
        db_session.close()

app.mount("/", socket_app)

@app.get("/")
async def home():
    logger.info("Home page accessed")
    return {"message": "Welcome to the home page!"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting UVicorn server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
