# app/models/model.py
from sqlalchemy import Column, Integer, String, DateTime, func
from app.database.database import Base
from sqlalchemy.orm import relationship


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    filename = Column(String)
    created_at = Column(DateTime, default=func.now())
