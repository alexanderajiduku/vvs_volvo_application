import cv2
import pickle
import numpy as np
import os

class CameraFeedUndistorter:
    CALIBRATION_DIR = "calibrations"
    CAMERA_MATRIX_FILE = 'cameramatrix.pkl'
    DIST_COEFFS_FILE = 'dist.pkl'
    
    def __init__(self):
        self.camera_matrix_file_path = os.path.join(self.CALIBRATION_DIR, self.CAMERA_MATRIX_FILE)
        self.dist_coeffs_file_path = os.path.join(self.CALIBRATION_DIR, self.DIST_COEFFS_FILE)

        self.load_calibration_parameters()

    def load_calibration_parameters(self):
        try:
            with open(self.camera_matrix_file_path, 'rb') as file:
                self.camera_matrix = pickle.load(file)
            with open(self.dist_coeffs_file_path, 'rb') as file:
                self.dist_coeffs = pickle.load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Calibration file not found: {e}")

    def undistort_frame(self, frame):
        h, w = frame.shape[:2]
        new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(np.array(self.camera_matrix), np.array(self.dist_coeffs), (w, h), 0)
        undistorted_frame = cv2.undistort(frame, np.array(self.camera_matrix), np.array(self.dist_coeffs), None, new_camera_matrix)
        return undistorted_frame