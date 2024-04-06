import os
import cv2
from camera_feed_handler import CameraHandler
from yolo_segmentation_process import YOLOSegmentation
from object_detection_segemntation import DetectionHandler  
from undistortion_class import CameraFeedUndistorter
from preprocessing import  preprocess_frame_func

def main():
    model_path = "best_version_2.pt"
    snapped_folder = "snapped_measured_trucks"
    calibration_file_path = "modularized/calibration_parameters/calibration.pkl"
    dist_coeffs_file_path = "modularized/calibration_parameters/dist.pkl"
    camera_matrix_file_path = "modularized/calibration_parameters/cameraMatrix.pkl"
    input_video_path = "test_videos/calibration_video5.mp4"
    confidence_threshold = 0.9
    capture_range = 10
    roi_dimensions = (0, 0, 800, 470)  

    if not os.path.exists(snapped_folder):
        os.makedirs(snapped_folder)

    yolo_segmentation = YOLOSegmentation(model_path)
    undistorter = CameraFeedUndistorter(calibration_file_path, dist_coeffs_file_path, camera_matrix_file_path)
    detection_processor = DetectionHandler(yolo_segmentation, roi_dimensions, snapped_folder, confidence_threshold, capture_range)

    def process_frame(frame, _):
        undistorted_frame = undistorter.undistort_frame(frame)
        frame_height, frame_width = undistorted_frame.shape[:2]
        preprocessed_frame, frame_width, frame_height= preprocess_frame_func(undistorted_frame)
        center_x = frame_width // 2
        center_y = frame_height // 2
        roi_height = 800  
        roi_width = int(470 * 1.3) 
        startX = max(0, center_x - roi_width // 2)
        startY = max(0, center_y - roi_height // 2 - 50) 
        endX = min(frame_width, startX + roi_width)
        endY = min(frame_height, startY + roi_height)
        _, _, seg_contours, scores = yolo_segmentation.detect(preprocessed_frame)
        center_coords = (center_x, center_y)    
        detection_processor._process_detections(frame, seg_contours, scores, startX, startY, endX, endY, center_coords)
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
        line_start = (startX + (roi_width // 2), startY)
        line_end = (startX + (roi_width // 2), endY)
        cv2.line(frame, line_start, line_end, (0, 255, 255), 2)  
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return True


    camera_handler = CameraHandler(process_frame_func=process_frame, snapped_folder=snapped_folder)
    camera_handler.set_feed_mode('file')
    camera_handler.start_feed(input_video_path)

if __name__ == "__main__":
    main()
