from pydantic import BaseModel
from datetime import datetime

class VehicleDetailBase(BaseModel):
    vehicle_id: str
    height: int
   

class VehicleDetailCreate(VehicleDetailBase):
    pass

class VehicleDetailResponse(VehicleDetailBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
