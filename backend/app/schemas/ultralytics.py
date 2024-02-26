from pydantic import BaseModel
from datetime import datetime

class UploadImageResponse(BaseModel):
    filename: str
    content_type: str
    file_path: str

    class Config:
        orm_mode = True



  

