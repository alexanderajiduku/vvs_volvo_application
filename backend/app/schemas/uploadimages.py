from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UploadImageResponse(BaseModel):
    filename: str
    content_type: str
    file_path: str
    camera_id: Optional[int]

class Config:
        orm_mode = True  
