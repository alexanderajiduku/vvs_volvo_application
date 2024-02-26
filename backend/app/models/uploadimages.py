from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.database.database import Base
from sqlalchemy.orm import relationship

class UploadedFile(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content_type = Column(String)
    upload_timestamp = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String)
    camera_id = Column(Integer, ForeignKey('camera.id'))  

    camera = relationship("Camera", back_populates="images")
