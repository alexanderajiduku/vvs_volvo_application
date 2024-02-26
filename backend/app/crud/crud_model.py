# app/crud/crud_model.py
from typing import List
from sqlalchemy.orm import Session
from app.models.model import Model  
from app.schemas.model import ModelCreate  

class CRUDModel:
    @staticmethod
    def create_with_file(db: Session, *, obj_in: ModelCreate, filename: str) -> Model:
        """
        Create a new database record and associated file.
        """
        db_obj = Model(name=obj_in.name, description=obj_in.description, filename=filename)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> List[Model]:
        """
        Retrieve multiple records with pagination.
        """
        return db.query(Model).offset(skip).limit(limit).all()
