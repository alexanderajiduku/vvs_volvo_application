from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from app.database.database import get_db  
from app.models.uploadimages import UploadedFile  
router = APIRouter()

@router.get("/images/{image_id}", response_class=FileResponse)
async def get_image(image_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific image by its ID.

    Parameters:
    - image_id (int): The ID of the image to retrieve.
    - db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
    - FileResponse: The file response containing the image.

    Raises:
    - HTTPException: If the image with the specified ID is not found.
    """
    image = db.query(UploadedFile).filter(UploadedFile.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(path=image.file_path, filename=image.filename)