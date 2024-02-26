# app/schemas/model.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ModelBase(BaseModel):
    name: str
    description: str

class ModelCreate(ModelBase):
    pass  

class ModelUpdate(ModelBase):
    pass  

class ModelInDBBase(ModelBase):
    """
    Base class for models stored in the database.
    """

    id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Model(ModelInDBBase):
    pass 
