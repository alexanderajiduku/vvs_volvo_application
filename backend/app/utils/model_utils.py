from sqlalchemy.orm import Session
from app.models.model import Model
from fastapi import HTTPException
import os

def get_model_path_from_db_or_config(model_id: int, db: Session) -> str:
    """
    Retrieves the path of a model from the database or configuration.

    Args:
        model_id (int): The ID of the model to retrieve.
        db (Session): The database session.

    Returns:
        str: The path of the model.

    Raises:
        HTTPException: If the model is not found in the database.
    """
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    model_directory = "uploaded_models" 
    model_path = os.path.join(model_directory, model.filename)

    return model_path


