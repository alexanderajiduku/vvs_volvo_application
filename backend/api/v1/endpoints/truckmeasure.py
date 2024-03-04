from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.vehicle_measure import VehicleDetectionService  # Adjust the import path as needed
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

    # Save the uploaded video file
    input_file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.{file_extension}")
    with open(input_file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process the video file for truck measurement
    output_file_path = vehicle_detection_service.process_video(input_file_path)

    # Return the processed video file
    return FileResponse(output_file_path, media_type="application/octet-stream", filename=os.path.basename(output_file_path))
