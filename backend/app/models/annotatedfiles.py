from sqlalchemy import Column, Integer, String, DateTime, func
from app.database.database import Base 

class AnnotatedFile(Base):
    __tablename__ = "annotated_files"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String, index=True)
    annotated_filename = Column(String)
    annotated_filepath = Column(String)
    created_at = Column(DateTime, default=func.now())
