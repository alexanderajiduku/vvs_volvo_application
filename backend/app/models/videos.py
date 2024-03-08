from sqlalchemy import Column, Integer, String
from app.database.database import Base  # Adjust the import based on your project structure
import datetime
from sqlalchemy import DateTime

class VideoModel(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, index=True) 
    file_path = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
