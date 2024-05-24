from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models.vehicledetails import VehicleDetail
from app.schemas.vehicledetails import VehicleDetailResponse

router = APIRouter()

@router.get("/vehicle-details", response_model=List[VehicleDetailResponse])
async def get_vehicle_details(db: Session = Depends(get_db)):
    vehicle_details = db.query(VehicleDetail).all()
    return vehicle_details
