"""
import cv2
import numpy as np
import pickle
import os
import datetime
from vmbpy import *
from yolo_segmentation import YOLOSegmentation
import sqlite3

class CameraFeedUndistorter:
    def __init__(self, calibration_file_path, dist_coeffs_file_path, camera_matrix_file_path, brightness=100):
        self.calibration_file_path = calibration_file_path
        self.dist_coeffs_file_path = dist_coeffs_file_path
        self.camera_matrix_file_path = camera_matrix_file_path
        self.brightness = brightness
        self.camera_matrix, self.dist_coeffs = self.load_calibration_parameters()

    def load_calibration_parameters(self):
        with open(self.camera_matrix_file_path, 'rb') as file:
            camera_matrix = pickle.load(file)
        with open(self.dist_coeffs_file_path, 'rb') as file:
            dist_coeffs = pickle.load(file)
        return camera_matrix, dist_coeffs

    def undistort_frame(self, frame):
        h, w = frame.shape[:2]
        new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(np.array(self.camera_matrix), np.array(self.dist_coeffs), (w, h), 0)
        undistorted_frame = cv2.undistort(frame, np.array(self.camera_matrix), np.array(self.dist_coeffs), None, new_camera_matrix)
        undistorted_frame = cv2.convertScaleAbs(undistorted_frame, alpha=self.brightness / 30, beta=0)
        return undistorted_frame

class VehicleDatabase:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS vehicle_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        serial_no TEXT,
                        time_detected TEXT,
                        vehicle_height REAL
                    )''')
        self.conn.commit()

    def insert_data(self, serial_no, time_detected, vehicle_height):
        c = self.conn.cursor()
        c.execute('''INSERT INTO vehicle_data (serial_no, time_detected, vehicle_height) 
                     VALUES (?, ?, ?)''', (serial_no, time_detected, vehicle_height))
        self.conn.commit()

    def close(self):
        self.conn.close()

def main():
    calibration_file_path = 'calibration.pkl'
    dist_coeffs_file_path = 'dist.pkl'
    camera_matrix_file_path = 'cameramatrix.pkl'
    model_path = "best9.pt"
    save_dir = 'snapshots_videos_images'
    line_x_position = 750
    brightness_level = 130
    serial_no = "ABC123"
    snapshot_taken = False

    os.makedirs(save_dir, exist_ok=True)
    video_save_path = os.path.join(save_dir, 'recorded_video333.avi')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(video_save_path, fourcc, 5.0, (1200, 700))

    undistorter = CameraFeedUndistorter(calibration_file_path, dist_coeffs_file_path, camera_matrix_file_path, brightness_level)
    yolo_segmentation = YOLOSegmentation(model_path)
    db = VehicleDatabase('vehicle_data.db')

    with VmbSystem.get_instance() as vimba:
        cameras = vimba.get_all_cameras()
        if not cameras:
            print('No cameras found')
            return

        with cameras[0] as cam:
            if cam.get_pixel_format() != PixelFormat.Mono8:
                try:
                    cam.set_pixel_format(PixelFormat.Bgr8)
                except Exception as e:
                    print("Error setting pixel format:", e)
                    return
            while True:
                frame = cam.get_frame()
                img = frame.as_opencv_image()
                undistorted_img = undistorter.undistort_frame(img)

                _, _, seg_contours, scores = yolo_segmentation.detect(undistorted_img)
                cv2.line(undistorted_img, (line_x_position, 0), (line_x_position, img.shape[0]), (255, 0, 0), 2)

                for seg, score in zip(seg_contours, scores):
                    if score > 0.90 and not snapshot_taken:  # High confidence scores indicating trucks and snapshot not taken
                        cv2.drawContours(undistorted_img, [seg], -1, (0, 255, 0), 2)
                        min_x = np.min(seg[:, 0])
                        max_x = np.max(seg[:, 0])
                        mask_height_pixels = np.max(seg[:, 1]) - np.min(seg[:, 1])
                        cv2.putText(undistorted_img, f'Mask Height: {mask_height_pixels}px', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                        #pixel_to_cm_ratio =4.7636  if mask_height_pixels <= 1650 else 5
                        if mask_height_pixels <= 1600:    #### 339,
                            pixel_to_cm_ratio = 4.7636
                        elif 1601 < mask_height_pixels <= 1650:
                            pixel_to_cm_ratio = 4.91044 
                        elif 1651 < mask_height_pixels <= 1700:
                            pixel_to_cm_ratio = 4.92
                        elif 1701 < mask_height_pixels <= 1750:
                            pixel_to_cm_ratio = 4.961
                        elif 1751 < mask_height_pixels <= 1800:
                            pixel_to_cm_ratio = 4.866
                        elif 1800 < mask_height_pixels <= 1850:
                            pixel_to_cm_ratio = 4.866
                        elif 1851 < mask_height_pixels <= 1900:
                            pixel_to_cm_ratio = 4.8469
                        elif 1901 < mask_height_pixels <= 1920:
                            pixel_to_cm_ratio = 4.882
                        elif 1921 < mask_height_pixels <= 1950:
                            pixel_to_cm_ratio = 4.8019
                        else:
                            pixel_to_cm_ratio = 5
                        mask_height_cm = mask_height_pixels / pixel_to_cm_ratio
                        
                        
                        cv2.putText(undistorted_img, f'Mask Height: {mask_height_cm:.2f} cm', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        if min_x <= line_x_position <= max_x:
                            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            snapshot_path = os.path.join(save_dir, f'snapshot_{timestamp}.jpg')
                            cv2.imwrite(snapshot_path, undistorted_img)
                            print(f"Snapshot taken at {timestamp} and saved to {snapshot_path}")
                            db.insert_data(serial_no, timestamp, mask_height_cm)
                            snapshot_taken = True  # Set to True after taking snapshot

                video_writer.write(cv2.resize(undistorted_img, (1200, 700)))  # Resize for consistent video frame size
                undistorted_img_resized = cv2.resize(undistorted_img, (1200, 800))
                cv2.imshow('Resized Undistorted Camera Feed - Press q to exit', undistorted_img_resized)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    video_writer.release()
    cv2.destroyAllWindows()
    db.close()

if __name__ == '__main__':
    main()
    
    
    
"""