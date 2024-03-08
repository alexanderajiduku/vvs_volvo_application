import logging
from fastapi import WebSocket, APIRouter, Depends, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.vehicle_measure import VehicleDetectionService
from app.models.videos import VideoModel
import os


logger = logging.getLogger(__name__)
UPLOAD_DIR = "truckmeasure_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
Base = declarative_base()


router = APIRouter()

@router.websocket("/ws/vehicle-heights/{model_id}/{video_id}")
async def websocket_endpoint(websocket: WebSocket, model_id: int, video_id: int, db: AsyncSession = Depends(get_db)):
    logger.debug(f"WebSocket connection attempt for model_id: {model_id}, video_id: {video_id}")
    await websocket.accept()

    try:
        video_info = db.query(VideoModel).filter(VideoModel.id == video_id, VideoModel.model_id == model_id).first()
        if video_info:
            input_source = video_info.file_path 
            vehicle_detection_service = VehicleDetectionService(model_id=model_id, db_session=db, output_dir=UPLOAD_DIR, detected_frames_dir=UPLOAD_DIR)
            await vehicle_detection_service.process_video_with_websocket(input_source, websocket)
            while True:
                data = await websocket.receive_text()
                if data == 'close':
                    break
        else:
            await websocket.send_text("Video information not found for the given video_id.")

    except WebSocketDisconnect:
        print(f"WebSocket disconnected for model_id: {model_id}, video_id: {video_id}")
    logger.debug(f"Video info: {video_info}")