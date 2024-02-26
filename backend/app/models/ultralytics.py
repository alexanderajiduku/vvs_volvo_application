from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.database.database import Base


class UploadedImages(Base):
    __tablename__ = 'ultralyticsuploads'
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content_type = Column(String)
    file_path = Column(String)
    upload_timestamp = Column(DateTime, default=datetime.utcnow)


    
    
    