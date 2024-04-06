import cv2
import pickle
import numpy as np

class CameraFeedUndistorter:
    def __init__(self, calibration_file_path, dist_coeffs_file_path, camera_matrix_file_path):
        self.calibration_file_path = calibration_file_path
        self.dist_coeffs_file_path = dist_coeffs_file_path
        self.camera_matrix_file_path = camera_matrix_file_path

        self.load_calibration_parameters()

    def load_calibration_parameters(self):
        with open(self.camera_matrix_file_path, 'rb') as file:
            self.camera_matrix = pickle.load(file)
        with open(self.dist_coeffs_file_path, 'rb') as file:
            self.dist_coeffs = pickle.load(file)

    def undistort_frame(self, frame):
        h, w = frame.shape[:2]
        new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(np.array(self.camera_matrix), np.array(self.dist_coeffs), (w, h), 0)
        undistorted_frame = cv2.undistort(frame, np.array(self.camera_matrix), np.array(self.dist_coeffs), None, new_camera_matrix)
        return undistorted_frame