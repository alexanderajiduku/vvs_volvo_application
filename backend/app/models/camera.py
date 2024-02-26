from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base 
from sqlalchemy.orm import relationship


class Camera(Base):
    __tablename__ = 'camera'

    id = Column(Integer, primary_key=True, index=True)
    camera_name = Column(String, index=True)
    camera_model = Column(String)
    checkerboard_width = Column(Integer)
    checkerboard_height = Column(Integer)
    description = Column(String)

    calibrationdata = relationship("CalibrationData", back_populates="camera")
    images = relationship("UploadedFile", back_populates="camera")  # Added relationship for UploadedFile
