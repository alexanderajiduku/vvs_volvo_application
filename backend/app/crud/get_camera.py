from sqlalchemy.orm import Session
from app.models.camera import Camera 

def get_camera(db: Session, camera_id: int):
    return db.query(Camera).filter(Camera.id == camera_id).first()
