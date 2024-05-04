from fastapi import APIRouter, Depends, HTTPException
from app.services.calibration_service import CameraCalibrationService
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.schemas.calibration import CalibrationResponse  

router = APIRouter()

@router.post("/calibration/{camera_id}", response_model=CalibrationResponse)
async def calibrate_camera(camera_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to calibrate a camera.

    Parameters:
    - camera_id (int): The ID of the camera to calibrate.
    - db (Session): The database session.

    Returns:
    - dict: A dictionary containing the message "Calibration successful" and the path to the calibration file.
    """
    try:
        calibration_service = CameraCalibrationService(db, camera_id)
        camera_matrix_path, dist_coeffs_path = calibration_service.perform_calibration()  
        return CalibrationResponse(
            message="Calibration successful", 
            camera_matrix_path=camera_matrix_path,
            dist_coeffs_path=dist_coeffs_path
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
