import logging.config
from my_logging_config import LOGGING_CONFIG
from fastapi import File, UploadFile, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.models.uploadimages import UploadedFile
from app.schemas.uploadimages import UploadImageResponse
from sqlalchemy.exc import SQLAlchemyError
import traceback
from my_logging_config import LOGGING_CONFIG
from app.database.database import get_db
from app.models.camera import Camera
import os
import shutil
import uuid


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

router = APIRouter()

UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

@router.post("/uploadimages/{camera_id}", response_model=UploadImageResponse)
async def upload_image(camera_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):

    try:
        camera = db.query(Camera).filter_by(id=camera_id).first()
        if not camera:
            raise HTTPException(status_code=404, detail="Camera not found")
        filename = str(uuid.uuid4()) + "_" + file.filename
        file_path = os.path.join(UPLOADS_DIR, filename)
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        uploaded_file = UploadedFile(
            filename=filename,
            content_type=file.content_type,
            file_path=file_path,
            camera_id=camera.id  
        )
        db.add(uploaded_file)
        db.flush() 
        db.commit() 
        db.refresh(uploaded_file) 
        record = db.query(UploadedFile).filter_by(filename=filename).first()
        if record:
            logger.info(f"Record found: {record.filename}")
        else:
            logger.error("Record not found after commit.")

        return {
            "filename": filename, 
            "content_type": file.content_type, 
            "file_path": file_path
        }
    except SQLAlchemyError as e:  
        db.rollback()  
        logger.error(f"Database transaction failed: {e}")
        raise HTTPException(status_code=500, detail="Database transaction failed.")
    
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        logger.debug(traceback.format_exc()) 
        raise HTTPException(status_code=500, detail=f"Error uploading file: {e}")
