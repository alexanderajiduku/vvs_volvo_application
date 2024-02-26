import cv2
import numpy as np
import logging
from sqlalchemy.exc import SQLAlchemyError
from app.models.calibrationdata import CalibrationData
from app.utils.image_utils import load_images
from sqlalchemy.orm import Session
from app.models.uploadimages import UploadedFile
from app.models.camera import Camera
import os
import time

class CameraCalibrationService:
    """
    Service class for camera calibration.

    Args:
        db (Session): The database session.
        camera_id (int): The ID of the camera.

    Attributes:
        UPLOADS_DIR (str): The directory for uploads.
        CALIBRATION_SUBDIR (str): The subdirectory for calibration data.
        db (Session): The database session.
        camera_id (int): The ID of the camera.
        calib_data_path (str): The path to the calibration data directory.
        image_paths (List[str]): The paths of the uploaded images.
        checkerboard_dims (Tuple[int, int]): The dimensions of the checkerboard.

    Methods:
        get_calibration_data_path: Get the path to the calibration data directory.
        fetch_checkerboard_dims: Fetch the dimensions of the checkerboard from the database.
        fetch_image_paths: Fetch the paths of the uploaded images from the database.
        find_checkerboard_corners: Find the checkerboard corners in the images.
        calibrate_camera: Calibrate the camera using the checkerboard corners.
        save_calibration_parameters: Save the calibration parameters to a file.
        save_calibration_data_to_db: Save the calibration data to the database.
        perform_calibration: Perform the camera calibration process.
    """

    UPLOADS_DIR = "calibrations"  
    CALIBRATION_SUBDIR = "calibration_data"

    def __init__(self, db: Session, camera_id: int):
        self.db = db
        self.camera_id = camera_id
        self.calib_data_path = self.get_calibration_data_path()
        self.image_paths = self.fetch_image_paths()
        self.checkerboard_dims = self.fetch_checkerboard_dims()

    def get_calibration_data_path(self):
        """
        Get the path to the calibration data directory.

        Returns:
            str: The path to the calibration data directory.
        """
        calib_dir = os.path.join(self.UPLOADS_DIR, self.CALIBRATION_SUBDIR)
        os.makedirs(calib_dir, exist_ok=True)
        
        return calib_dir

    def fetch_checkerboard_dims(self):
        """
        Fetch the dimensions of the checkerboard from the database.

        Returns:
            Tuple[int, int]: The dimensions of the checkerboard.
        
        Raises:
            ValueError: If the camera with the specified ID is not found in the database.
        """
        try:
            camera_info = self.db.query(Camera).filter(Camera.id == self.camera_id).first()
            if not camera_info:
                raise ValueError(f"Camera with ID {self.camera_id} not found in the database.")
            return (camera_info.checkerboard_height, camera_info.checkerboard_width)
        except SQLAlchemyError as e:
            logging.error(f"Database error when fetching checkerboard dimensions: {str(e)}")
            raise

    def fetch_image_paths(self):
        """
        Fetch the paths of the uploaded images from the database.

        Returns:
            List[str]: The paths of the uploaded images.
        
        Raises:
            ValueError: If no uploaded images are found in the database.
        """
        try:
            image_records = self.db.query(UploadedFile).all()
            if not image_records:
                raise ValueError("No uploaded images found in the database.")
            return [image_record.file_path for image_record in image_records]
        except SQLAlchemyError as e:
            logging.error(f"Database error when fetching image paths: {str(e)}")
            raise

 
