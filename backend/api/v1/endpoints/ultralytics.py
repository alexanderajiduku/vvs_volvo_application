from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.ultralytics import UploadedImages
from app.models.annotatedfiles import AnnotatedFile as AnnotatedFileModel
from app.schemas.AnnotatedFile import AnnotatedFile
from app.services.ultralytics import YOLOService
import os
import shutil
import uuid
import cv2
from typing import Any
from PIL import Image
import numpy as np


router = APIRouter()

UPLOAD_DIR = "ultralytics_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/inference/{model_id}")
async def upload_file(model_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Uploads a file for YOLO inference and annotation.

    Parameters:
    - model_id (int): The ID of the YOLO model to use for inference.
    - file (UploadFile): The file to be uploaded for inference.
    - db (Session): The database session.

    Returns:
    - dict: A dictionary containing the uploaded file information and the detection results.
    """
    try:
        yolo_service = YOLOService(model_id=model_id, db_session=db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in ['jpg', 'mp4']:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    uploaded_image = UploadedImages(filename=filename, content_type=file.content_type, file_path=file_path)
    db.add(uploaded_image)
    db.commit()
    db.refresh(uploaded_image)

    if file_extension == 'jpg':
        detection_results = yolo_service.predict_and_annotate_image(file_path)
    elif file_extension == 'mp4':
        detection_results = yolo_service.predict_and_annotate_video(file_path)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type for YOLO processing")

    annotated_file_key = os.path.basename(detection_results["annotated_filename"])

    annotated_file = AnnotatedFileModel(
        original_filename=filename,
        annotated_filename=annotated_file_key,
        annotated_filepath=detection_results["annotated_filepath"]
    )
    db.add(annotated_file)
    db.commit()
    db.refresh(annotated_file)

    return {
        "filename": filename,
        "content_type": file.content_type,
        "annotated_file_key": annotated_file_key,
        **detection_results
    }

@router.get("/video-stream/{filename:path}")
async def video_stream(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return StreamingResponse(get_frame_generator(file_path), media_type="multipart/x-mixed-replace;boundary=frame")

def get_frame_generator(video_path: str):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    cap.release()

@router.get("/webcam_feed")
async def webcam_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace;boundary=frame")

def generate_frames():
    cap = cv2.VideoCapture(0) # 0 is the default camera
    while True:
        success, frame = cap.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    cap.release()

@router.get("/annotated-files/{file_id}", response_model=AnnotatedFile)
def get_annotated_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(AnnotatedFileModel).filter(AnnotatedFileModel.id == file_id).first()
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file

