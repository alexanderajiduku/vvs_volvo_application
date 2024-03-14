from fastapi import APIRouter, HTTPException
import logging
from app.services.vehicle_measure import VehicleDetectionService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/video/start-video-capture")
async def start_video_capture(input_source: str = '0'):
    try:
        # Assuming `detection_model`, `tracker`, `output_dir`, and `detected_frames_dir` are available
        await VehicleDetectionService.process_video(input_source)
        return {"message": "Video capture started successfully"}
    except Exception as e:
        logger.error(f"Error starting video capture: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
