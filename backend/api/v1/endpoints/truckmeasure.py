from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.vehicle_measure import VehicleDetectionService 
from app.models.vehicledetails import VehicleDetail
from app.utils.camera_utils import active_camera_handlers
import logging
from app.services.camera_handler import CameraHandler
import os
import shutil
import uuid

router = APIRouter()

UPLOAD_DIR = "truckmeasure_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
global current_vehicle_detection_service

@router.post("/process-truck-measure/{model_id}")
async def process_truck_measure_endpoint(model_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    vehicle_detection_service = VehicleDetectionService(model_id, db, UPLOAD_DIR, UPLOAD_DIR)
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
    logging.info(f"Starting camera with ID {camera_id}")
    vehicle_detection_service = VehicleDetectionService(model_id, db, UPLOAD_DIR, UPLOAD_DIR)
    await vehicle_detection_service.process_video(str(camera_id))
    logging.info(f"Camera {camera_id} started successfully. Adding to active_camera_handlers.")
    camera_handler = CameraHandler(camera_id=camera_id)
    camera_handler.start_camera()
    active_camera_handlers[str(camera_id)] = camera_handler
    logging.info(f"CameraHandler for camera ID {camera_id} added to active_camera_handlers.")
    logging.debug(f"Current active_camera_handlers: {list(active_camera_handlers.keys())}")
    return {"message": f"Camera {camera_id} feed is being processed and heights are being saved."}


@router.post("/process-truck-measure/{model_id}/{camera_id}")
async def process_truck_measure_endpoint_camera(model_id: int, camera_id: int, db: Session = Depends(get_db)):
    try:
        logging.info(f"Starting camera with ID {camera_id}")
        camera_handler = CameraHandler(camera_id=camera_id)
        camera_handler.start_camera()
        active_camera_handlers[str(camera_id)] = camera_handler
        logging.info(f"CameraHandler for camera ID {camera_id} added to active_camera_handlers.")
        vehicle_detection_service = VehicleDetectionService(model_id, db, UPLOAD_DIR, UPLOAD_DIR)
        await vehicle_detection_service.process_video(str(camera_id))
        return {"message": f"Camera {camera_id} feed is being processed and heights are being saved."}
    except Exception as e:
        logging.error(f"Error starting camera with ID {camera_id}: {e}")
        return {"error": f"Failed to start camera with ID {camera_id}: {e}"}




@router.post("/stop-camera-feed/{camera_id}")
async def stop_camera_feed(camera_id: int):
    try:
        logging.debug(f"Attempting to stop camera with ID: {camera_id}")
        logging.debug(f"Current active_camera_handlers: {list(active_camera_handlers.keys())}")
        camera_id_str = str(camera_id)  
        camera_handler = active_camera_handlers.get(camera_id_str)
        if not camera_handler:
            logging.warning(f"No active camera handler found for ID: {camera_id}")
            raise ValueError(f"No active camera found for camera ID {camera_id}")
        camera_handler.stop_camera()
        del active_camera_handlers[camera_id_str]
        logging.info(f"Camera feed for camera ID {camera_id} has been stopped.")
        logging.debug(f"Current active_camera_handlers after removal: {list(active_camera_handlers.keys())}")
        return {"message": f"Camera feed for camera ID {camera_id} has been stopped."}
    except Exception as e:
        logging.error(f"Error stopping camera feed for camera ID {camera_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to stop camera feed for camera ID {camera_id}")



@router.get("/stream-processed-video/{model_id}")
async def stream_processed_video_endpoint(model_id: int, input_source: str = Query(...), db: Session = Depends(get_db)):
    vehicle_detection_service = VehicleDetectionService(model_id=model_id, db_session=db, output_dir=UPLOAD_DIR, detected_frames_dir=UPLOAD_DIR)
    frame_generator = vehicle_detection_service.stream_video(input_source=input_source)
    return StreamingResponse(frame_generator, media_type="multipart/x-mixed-replace; boundary=frame")

@router.get("/latest-heights")
async def get_latest_heights(db: Session = Depends(get_db)):
    heights = db.query(VehicleDetail).order_by(VehicleDetail.id.desc()).limit(10).all()
    return heights
