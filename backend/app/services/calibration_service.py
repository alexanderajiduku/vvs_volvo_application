import cv2
import numpy as np
import logging
import pickle
from sqlalchemy.exc import SQLAlchemyError
from app.models.calibrationdata import CalibrationData
from app.utils.image_utils import load_images
from sqlalchemy.orm import Session
from app.models.uploadimages import UploadedFile
from app.models.camera import Camera
import json
import os
import time

class CameraCalibrationService:
    UPLOADS_DIR = "calibrations"  # Base directory for uploads
    CALIBRATION_SUBDIR = "calibration_data"

    def __init__(self, db: Session, camera_id: int):
        self.db = db
        self.camera_id = camera_id
        self.calib_data_path = self.get_calibration_data_path()
        self.image_paths = self.fetch_image_paths()
        self.checkerboard_dims = self.fetch_checkerboard_dims()

    def get_calibration_data_path(self):
        calib_dir = os.path.join(self.UPLOADS_DIR, self.CALIBRATION_SUBDIR)
        os.makedirs(calib_dir, exist_ok=True)
        
        return calib_dir

    def fetch_checkerboard_dims(self):
        try:
            camera_info = self.db.query(Camera).filter(Camera.id == self.camera_id).first()
            if not camera_info:
                raise ValueError(f"Camera with ID {self.camera_id} not found in the database.")
            return (camera_info.checkerboard_height, camera_info.checkerboard_width)
        except SQLAlchemyError as e:
            logging.error(f"Database error when fetching checkerboard dimensions: {str(e)}")
            raise

    def fetch_image_paths(self):
        try:
            image_records = self.db.query(UploadedFile).all()
            if not image_records:
                raise ValueError("No uploaded images found in the database.")
        # Replace 'path' with the correct attribute name, e.g., 'file_path'
            return [image_record.file_path for image_record in image_records]
        except SQLAlchemyError as e:
            logging.error(f"Database error when fetching image paths: {str(e)}")
            raise


    def find_checkerboard_corners(self, images):
        objpoints = []  
        imgpoints = []  
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        objp = np.zeros((self.checkerboard_dims[0] * self.checkerboard_dims[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0:self.checkerboard_dims[0], 0:self.checkerboard_dims[1]].T.reshape(-1, 2)

        for img in images:
            try:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            except cv2.error as e:
                logging.error(f"OpenCV error in converting image to grayscale: {str(e)}")
                continue  
            ret, corners = cv2.findChessboardCorners(gray, (self.checkerboard_dims[0], self.checkerboard_dims[1]), None)
            if ret:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)

        if not objpoints or not imgpoints:
            raise ValueError("Could not find checkerboard corners in any of the images.")

        return objpoints, imgpoints

    def calibrate_camera(self, objpoints, imgpoints, image_shape):
        try:
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, image_shape[::-1], None, None)
            if not ret:
                raise ValueError("Camera calibration failed.")
            return {"ret": ret, "mtx": mtx, "dist": dist, "rvecs": rvecs, "tvecs": tvecs}
        except cv2.error as e:
            logging.error(f"OpenCV error during camera calibration: {str(e)}")
            raise ValueError("Error during camera calibration.")

    def save_calibration_parameters(self, params):
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            camera_matrix_filename = f"cameramatrix_{timestamp}.pkl"
            dist_coeffs_filename = f"dist_{timestamp}.pkl"
            camera_matrix_filepath = os.path.join(self.calib_data_path, camera_matrix_filename)
            dist_coeffs_filepath = os.path.join(self.calib_data_path, dist_coeffs_filename)

            if not os.path.exists(self.calib_data_path):
                os.makedirs(self.calib_data_path)
            
            with open(camera_matrix_filepath, 'wb') as f:
                pickle.dump(params["mtx"], f)
    
            with open(dist_coeffs_filepath, 'wb') as f:
                pickle.dump(params["dist"], f)
            
            self.save_calibration_data_to_db(camera_matrix_filepath, dist_coeffs_filepath)
            return camera_matrix_filepath, dist_coeffs_filepath

        except Exception as e:
            logging.error(f"Error when saving calibration parameters: {str(e)}")
            raise ValueError("Error when saving calibration parameters.")
 
        
    def save_calibration_data_to_db(self, camera_matrix_filepath, dist_coeffs_filepath):
        calibration_data = CalibrationData(
            camera_id=self.camera_id,
            calibration_file_path=json.dumps({
                "camera_matrix": camera_matrix_filepath,
                "dist_coeffs": dist_coeffs_filepath
            })
        )
        self.db.add(calibration_data)
        self.db.commit()

    def perform_calibration(self):
        try:
            images = load_images(self.image_paths)
            if not images:
                raise ValueError("No images loaded. Please check the image paths.")
            objpoints, imgpoints = self.find_checkerboard_corners(images)
            calibration_params = self.calibrate_camera(objpoints, imgpoints, images[0].shape[:2])
            return self.save_calibration_parameters(calibration_params)
        except Exception as e:
            logging.error(f"Error during camera calibration process: {str(e)}")
            raise ValueError(f"Calibration failed: {str(e)}")
        