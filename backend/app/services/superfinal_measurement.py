import cv2
import numpy as np
import pickle
import os
import datetime
from vmbpy import *
from yolo_segmentation import YOLOSegmentation

class CameraFeedUndistorter:
    def __init__(self, calibration_file_path, dist_coeffs_file_path, camera_matrix_file_path):
        self.calibration_file_path = calibration_file_path
        self.dist_coeffs_file_path = dist_coeffs_file_path
        self.camera_matrix_file_path = camera_matrix_file_path
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
        return undistorted_frame

def main():
    # Initialization
    calibration_file_path = 'calibration.pkl'
    dist_coeffs_file_path = 'dist.pkl'
    camera_matrix_file_path = 'cameramatrix.pkl'
    model_path = "best9.pt"
    save_dir = 'snapshots_starting'
    line_x_position = 750  # X position of the line for snapshot capture
    snapshot_taken = False  # Flag to check if snapshot has already been taken

    # Video recording parameters
    video_save_path = os.path.join(save_dir, 'recorded_video.avi')
    fps = 30.0  # Frames per second
    frame_size = (1280, 720)  # Frame size (width, height)

    # Ensure snapshot directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(video_save_path, fourcc, fps, frame_size)

    undistorter = CameraFeedUndistorter(calibration_file_path, dist_coeffs_file_path, camera_matrix_file_path)
    yolo_segmentation = YOLOSegmentation(model_path)

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

                # Write undistorted frame to video
                video_writer.write(undistorted_img)

                _, _, seg_contours, scores = yolo_segmentation.detect(undistorted_img)
                cv2.line(undistorted_img, (line_x_position, 0), (line_x_position, img.shape[0]), (255, 0, 0), 2)

                for seg, score in zip(seg_contours, scores):
                    if score > 0.90 and not snapshot_taken:  # High confidence scores indicating trucks and snapshot not taken
                        cv2.drawContours(undistorted_img, [seg], -1, (0, 255, 0), 2)
                        min_x = np.min(seg[:, 0])
                        max_x = np.max(seg[:, 0])
                        mask_height_pixels = np.max(seg[:, 1]) - np.min(seg[:, 1])

                        pixel_to_cm_ratio = 4.82025316 if mask_height_pixels <= 1500 else 4.7
                        mask_height_cm = mask_height_pixels / pixel_to_cm_ratio
                        
                        # Ensure drawing on the undistorted image
                        cv2.putText(undistorted_img, f'Mask Height: {mask_height_pixels}px', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.putText(undistorted_img, f'Mask Height: {mask_height_cm:.2f} cm', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        if min_x <= line_x_position <= max_x:
                            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            snapshot_path = os.path.join(save_dir, f'snapshot_{timestamp}.jpg')
                            cv2.imwrite(snapshot_path, undistorted_img)
                            print(f"Snapshot taken at {timestamp} and saved to {snapshot_path}")
                            snapshot_taken = True  # Set to True after taking snapshot

                undistorted_img_resized = cv2.resize(undistorted_img, (1200, 800))
                cv2.imshow('Resized Undistorted Camera Feed - Press q to exit', undistorted_img_resized)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    # Release video writer and close windows
    video_writer.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
