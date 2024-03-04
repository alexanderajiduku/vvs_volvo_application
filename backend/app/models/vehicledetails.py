from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from app.database.database import Base  # Ensure this import matches your project structure
from datetime import datetime
from sqlalchemy import DateTime

class VehicleDetail(Base):
    __tablename__ = 'vehicle_details'

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(String, index=True)
    height = Column(Float) 
    created_at = Column(DateTime, default=datetime.utcnow)