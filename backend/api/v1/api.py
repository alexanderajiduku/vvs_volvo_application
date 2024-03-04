from fastapi import APIRouter
from api.v1.endpoints import auth , uploadimages, calibration, camera, getuploadedimages, camera, model, videofeed, ultralytics, truckmeasure


api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(uploadimages.router, tags=["uploadimages"])
api_router.include_router(calibration.router, tags=["calibration"]) 
api_router.include_router(camera.router, tags=["camera"]) 
api_router.include_router(getuploadedimages.router, tags=["getuploadedimages"]) 
api_router.include_router(model.router, tags=["model"])
api_router.include_router(videofeed.router, tags=["videofeed"])
api_router.include_router(ultralytics.router, tags=["ultralytics"])
api_router.include_router(truckmeasure.router, tags=["truckmeasure"])

"""
This file defines the API router for the backend application.
It includes various routers for different endpoints such as authentication, image upload, calibration, camera, etc.
Each router is associated with specific tags for better organization and documentation.
"""
