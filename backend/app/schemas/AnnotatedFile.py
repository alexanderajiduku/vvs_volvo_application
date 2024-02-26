# schemas.py

from pydantic import BaseModel
from datetime import datetime

class AnnotatedFileBase(BaseModel):
    """
    Represents the base schema for an annotated file.

    Attributes:
        original_filename (str): The original filename of the file.
        annotated_filename (str): The annotated filename of the file.
        annotated_filepath (str): The annotated filepath of the file.
    """

    original_filename: str
    annotated_filename: str
    annotated_filepath: str

    class Config:
        orm_mode = True

class AnnotatedFileCreate(AnnotatedFileBase):
    pass

class AnnotatedFile(AnnotatedFileBase):
    id: int
    created_at: datetime
