from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.services.vehicle_measure_detector import DetectionHandler
from app.models.vehicledetails import VehicleDetail
from app.utils.camera_utils import active_camera_handlers
import logging
from app.services.camera_handler import CameraHandler
from app.schemas.vehicledetails import VehicleDetailResponse
import shutil
import uuid
import os

router = APIRouter()

UPLOAD_DIR = "truckmeasure_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/process-truck-measure/{model_id}")
async def process_truck_measure_endpoint(model_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    roi_settings = {
        "height": 800,  
        "width": int(470 * 1.3) 
    }
    vehicle_detection_service = DetectionHandler(
        model_id=model_id,
        db_session=db,  
        roi_settings = roi_settings,  
        snapped_folder=UPLOAD_DIR,
        confidence_threshold=0.9,  
        capture_range=10,  
        output_dir="processed_videos",  
        detected_frames_dir="detected_frames"  
    )
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in ['mp4', 'avi']:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    input_file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.{file_extension}")
    with open(input_file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    await vehicle_detection_service.process_video(input_file_path)
    return {"message": "Video is being processed and heights are being saved."}


@router.post("/process-truck-measure/{model_id}/{camera_id}")
async def process_truck_measure_endpoint_camera(model_id: int, camera_id: int, db: Session = Depends(get_db)):
    roi_settings = {
        "height": 800,  
        "width": int(470 * 1.3) 
    }
    logging.info(f"Starting camera with ID {camera_id}")
    vehicle_detection_service = DetectionHandler(
        model_id=model_id,
        db_session=db,  
        roi_settings = roi_settings,  
        snapped_folder=UPLOAD_DIR,
        confidence_threshold=0.9,  
        capture_range=10,  
        output_dir="processed_videos",  
        detected_frames_dir="detected_frames"  
    )
    await vehicle_detection_service.process_video(str(camera_id))
    logging.info(f"Camera {camera_id} started successfully. Adding to active_camera_handlers.")
    

@router.post("/stop-camera-feed/{camera_id}")
async def stop_camera_feed(model_id: int, camera_id: int, db: Session = Depends(get_db)):
    roi_settings = {
        "height": 800,  
        "width": int(470 * 1.3) 
    }
    vehicle_detection_service = DetectionHandler(
        model_id=model_id,
        db_session=db,  
        roi_settings = roi_settings,  
        snapped_folder=UPLOAD_DIR,
        confidence_threshold=0.9,  
        capture_range=10,  
        output_dir="processed_videos",  
        detected_frames_dir="detected_frames"  
    )
    await vehicle_detection_service.stop_processing(str(camera_id))
    try:
        if CameraHandler.is_active():
            CameraHandler.get_instance().stop_camera()
            logging.info("Camera feed has been stopped.")
            return {"message": "Camera feed has been stopped."}
        else:
            logging.warning("No active camera to stop.")
            return {"message": "No active camera to stop."}
    except Exception as e:
        logging.error(f"Error stopping camera feed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to stop camera feed")
    

