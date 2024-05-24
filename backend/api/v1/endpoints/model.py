
import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database.database import get_db
from app.schemas.model import Model as SchemaModel, ModelCreate, ModelResponse
from app.crud.crud_model import CRUDModel
from app.models.model import Model


router = APIRouter()

UPLOAD_DIR = "uploaded_models"
os.makedirs(UPLOAD_DIR, exist_ok=True)

crud_model = CRUDModel() 

@router.post("/model", response_model=SchemaModel)
async def create_model(
    *,
    db: Session = Depends(get_db),
    name: str,
    description: str,
    file: UploadFile = File(...)
):
    """
    Create a new model with the given name, description, and file.

    Parameters:
    - db: The database session dependency.
    - name: The name of the model.
    - description: The description of the model.
    - file: The file to be uploaded.

    Returns:
    - The created model.

    Raises:
    - HTTPException: If the file type is not allowed.
    """
   
    allowed_extensions = [".pt", ".pkl"]
    file_extension = os.path.splitext(file.filename)[1]
    
    if file_extension not in allowed_extensions:
       
        raise HTTPException(status_code=400, detail=f"File type '{file_extension}' is not allowed. Only {allowed_extensions} files are accepted.")

    filename = f"{name}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    model_in = ModelCreate(name=name, description=description)
    created_model = crud_model.create_with_file(db=db, obj_in=model_in, filename=filename)  
    return created_model

@router.get("/model", response_model=list[SchemaModel])
def read_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    models = crud_model.get_multi(db, skip=skip, limit=limit)
    return models


@router.post("/model/{model_id}/path")
async def get_model_path(model_id: int, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    
    if model is None:
        raise HTTPException(status_code=404, detail=f"Model with ID {model_id} not found")
    model_path = os.path.join('uploaded_models', model.filename)
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail=f"Model file for ID {model_id} not found at {model_path}")

    return {"model_path": model_path}

@router.delete("/model/{model_id}", response_model=ModelResponse)
async def delete_model(model_id: int, db: Session = Depends(get_db)):
    """
    Delete a model by ID.

    Parameters:
    - model_id: The ID of the model to delete.
    - db: The database session.

    Returns:
    - ModelResponse: The details of the deleted model.

    Raises:
    - HTTPException: If the model is not found.
    """
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # Delete the file associated with the model
    model_path = os.path.join(UPLOAD_DIR, model.filename)
    if os.path.exists(model_path):
        os.remove(model_path)
    
    # Delete the model from the database
    db.delete(model)
    db.commit()
    
    return ModelResponse(**model.__dict__)