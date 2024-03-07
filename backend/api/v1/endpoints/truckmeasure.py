from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.vehicle_measure import VehicleDetectionService 
from app.models.vehicledetails import VehicleDetail
import os
import shutil
import uuid

router = APIRouter()

UPLOAD_DIR = "truckmeasure_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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



@router.get("/stream-processed-video/{model_id}")
async def stream_processed_video_endpoint(model_id: int, input_source: str = Query(...), db: Session = Depends(get_db)):
    vehicle_detection_service = VehicleDetectionService(model_id=model_id, db_session=db, output_dir=UPLOAD_DIR, detected_frames_dir=UPLOAD_DIR)
    frame_generator = vehicle_detection_service.stream_video(input_source=input_source)
    return StreamingResponse(frame_generator, media_type="multipart/x-mixed-replace; boundary=frame")

@router.get("/latest-heights")
async def get_latest_heights(db: Session = Depends(get_db)):
    heights = db.query(VehicleDetail).order_by(VehicleDetail.id.desc()).limit(10).all()
    return heights
