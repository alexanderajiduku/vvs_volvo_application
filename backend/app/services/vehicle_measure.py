# services/vehicle_detection_service.py

import cv2
import numpy as np
import pandas as pd
import os
from typing import List, Dict
from .tracker import Tracker  
from sqlalchemy.orm import Session
from app.models.model import Model
from .yolo_segmentation import YOLOSegmentation  
from app.models.vehicledetails import VehicleDetail
from ultralytics import YOLO  



class VehicleDetectionService:
    def __init__(self, model_id: int, db_session: Session, output_dir: str = 'processed_videos', detected_frames_dir: str = 'detected_frames'):
        model = db_session.query(Model).filter(Model.id == model_id).first()
        if model is None:
            raise ValueError(f"Model with ID {model_id} not found in the database")
        model_path = os.path.join('uploaded_models', model.filename)  # Adjust the path as needed

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"YOLO model file not found at {model_path}")

        self.db_session = db_session
        self.detection_model = YOLO(model_path)
        self.segmentation_model = YOLOSegmentation(model_path)
        self.tracker = Tracker()
        self.output_dir = output_dir
        self.detected_frames_dir = detected_frames_dir

        # Ensure output directories exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(self.detected_frames_dir):
            os.makedirs(self.detected_frames_dir)

        
        self.class_list = [
    "person", "bicycle", "car", "motorcycle", "airplane",
    "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
    "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse",
    "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
    "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
    "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife",
    "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot",
    "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed",
    "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard",
    "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book",
    "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

        self.red_line_x = 198
        self.blue_line_x = 868
        self.center_line_x = (self.blue_line_x + self.red_line_x) // 2
        self.offset = 6
        self.vehicle_process = {}
        self.vehicle_display_info = {}
        self.display_duration = 60

    def process_video(self, input_video_path: str) -> str:
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            raise IOError("Could not open video file")

        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        output_video_path = os.path.join(self.output_dir, os.path.basename(input_video_path).split('.')[0] + '_processed.avi')
        out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (frame_width, frame_height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (1020, 500))
            self.detect_and_track(frame)
            self.draw_lines(frame)
            self.display_vehicle_info(frame)

            out.write(frame)

        cap.release()
        out.release()
        return output_video_path

    def detect_and_track(self, frame: np.ndarray):
        results = self.detection_model.predict(frame)
        boxes = results[0].boxes.data.detach().cpu().numpy()
        detections = pd.DataFrame(boxes).astype("float")

        detected_cars = [row[:4].astype(int).tolist() for index, row in detections.iterrows() if self.class_list[int(row[5])] == 'car']
        bbox_id = self.tracker.update(detected_cars)

        for bbox in bbox_id:
            x3, y3, x4, y4, id = bbox
            cx = int((x3 + x4) / 2)
            if self.center_line_x - self.offset < cx < self.center_line_x + self.offset and id not in self.vehicle_process:
                self.vehicle_process[id] = 'crossed'
                frame_path = os.path.join(self.detected_frames_dir, f'vehicle_{id}_center_line.jpg')
                cv2.imwrite(frame_path, frame)
                seg_img = cv2.imread(frame_path)
                if seg_img is not None:
                    seg_img = cv2.resize(seg_img, None, fx=0.7, fy=0.7)
                    _, _, seg_contours, _ = self.segmentation_model.detect(seg_img)
                    for seg in seg_contours:
                        y_coords = seg[:, 1]  
                        min_y = np.min(y_coords)
                        max_y = np.max(y_coords)
                        vertical_extent = int(max_y - min_y) 
                        new_height = VehicleDetail(vehicle_id=str(id), height=vertical_extent)
                        self.db_session.add(new_height)
        self.db_session.commit()

    def draw_lines(self, frame: np.ndarray):
        cv2.line(frame, (self.red_line_x, 0), (self.red_line_x, frame.shape[0]), (0, 0, 255), 2)
        cv2.line(frame, (self.blue_line_x, 0), (self.blue_line_x, frame.shape[0]), (255, 0, 0), 2)
        cv2.line(frame, (self.center_line_x, 0), (self.center_line_x, frame.shape[0]), (0, 255, 0), 2)

    def display_vehicle_info(self, frame: np.ndarray):
        completed_vehicles = len(self.vehicle_process)
        cv2.putText(frame, f'Completed Vehicles: {completed_vehicles}', (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        for obj_id, info in list(self.vehicle_display_info.items()):
            if info['display_frame_count'] > 0:
                cv2.putText(frame, f'ID {obj_id}: Height {info["vertical_extent"]}', info['position'], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                info['display_frame_count'] -= 1
            else:
                del self.vehicle_display_info[obj_id]
