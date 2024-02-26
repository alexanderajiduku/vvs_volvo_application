from sqlalchemy import Column, Integer, JSON, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from app.database.database import Base
from sqlalchemy.orm import relationship


class CalibrationData(Base):
    __tablename__ = "calibrationdata"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(Integer, ForeignKey('camera.id'), nullable=False)
    calibration_file_path = Column(String, nullable=False)
    
    camera = relationship("Camera", back_populates="calibrationdata")
