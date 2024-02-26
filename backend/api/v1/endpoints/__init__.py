# app/api/v1/endpoints/__init__.py
from fastapi import APIRouter
from . import auth, uploadimages as upload

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(upload.router)
