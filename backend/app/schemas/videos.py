from pydantic import BaseModel
from datetime import datetime

class VideoSchema(BaseModel):
    id: int
    model_id: int
    file_path: str
    created_at: datetime

    class Config:
        orm_mode = True
