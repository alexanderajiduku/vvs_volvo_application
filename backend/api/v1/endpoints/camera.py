from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.camera import Camera
from app.schemas.camera import CameraCreate, CameraResponse, CameraList
from app.database.database import get_db
from typing import List

router = APIRouter()

@router.post("/registercamera", response_model=CameraResponse)
async def register_camera(camera_data: CameraCreate, db: Session = Depends(get_db)):
    new_camera = Camera(**camera_data.dict())
    db.add(new_camera)
    db.commit()
    db.refresh(new_camera)
    return CameraResponse(**new_camera.__dict__)  


@router.get("/camera/{camera_id}", response_model=CameraList)  
async def get_camera(camera_id: int, db: Session = Depends(get_db)):
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return CameraList(**camera.__dict__)  


@router.delete("/camera/{camera_id}", response_model=CameraResponse)
async def delete_camera(camera_id: int, db: Session = Depends(get_db)):
    """
    Delete a camera by ID.

    Parameters:
    - camera_id: The ID of the camera to delete.
    - db: The database session.

    Returns:
    - CameraResponse: The details of the deleted camera.

    Raises:
    - HTTPException: If the camera is not found.
    """
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    db.delete(camera)
    db.commit()
    return CameraResponse(**camera.__dict__)

@router.get("/camera", response_model=List[CameraList])
async def get_all_cameras(db: Session = Depends(get_db)):
    """
    Retrieve a list of all cameras.

    Parameters:
    - db: The database session.

    Returns:
    - List[CameraList]: A list of CameraList objects representing the cameras.

    Raises:
    - HTTPException: If no cameras are found.
    """
    cameras = db.query(Camera).all()
    camera_list = [CameraList(**camera.__dict__) for camera in cameras]
    if not cameras:
        raise HTTPException(status_code=404, detail="No cameras found")
    return camera_list