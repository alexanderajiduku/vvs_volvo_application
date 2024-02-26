from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db 
from app.services.video_service import VideoService
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.get("/video-feed/{camera_id}")
async def video_feed(camera_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the video feed for a specific camera.

    Parameters:
    - camera_id (int): The ID of the camera.

    Returns:
    - StreamingResponse: The video feed as a streaming response.

    Raises:
    - HTTPException: If there is an error retrieving the video feed.
    """
    video_service = VideoService(0)
    try:
        return StreamingResponse(video_service.stream_video(camera_id), media_type="multipart/x-mixed-replace; boundary=frame")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
