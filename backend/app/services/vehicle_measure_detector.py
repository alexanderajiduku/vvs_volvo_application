import cv2
import numpy as np
import pandas as pd
import os 
from sqlalchemy.orm import Session
from app.models.model import Model
from .yolo_segmentation import YOLOSegmentation  
from app.models.vehicledetails import VehicleDetail
from app.services.camera_handler import CameraHandler
from .preprocessing import preprocess_frame_func
from app.utils.camera_utils import active_camera_handlers
from app.shared.shared import frames_queue
from typing import AsyncGenerator
from fastapi import WebSocket
import asyncio
import logging

class DetectionHandler:
    def __init__(self, model_id, db_session: Session, roi_settings, snapped_folder, confidence_threshold, capture_range, output_dir: str = 'processed_videos', detected_frames_dir: str = 'detected_frames'):
        model = db_session.query(Model).filter(Model.id == model_id).first()
        if model is None:
            raise ValueError(f"Model with ID {model_id} not found in the database")
        model_path = os.path.join('uploaded_models', model.filename)  
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"YOLO model file not found at {model_path}")
        
        self.db_session = db_session
        self.segmentation_model = YOLOSegmentation(model_path)
        self.roi_settings = roi_settings 
        self.snapped_folder = snapped_folder  
        self.confidence_threshold = confidence_threshold  
        self.capture_range = capture_range  
        self.crossed_ids = []  
        self.camera_handler = None 
        self.output_dir = output_dir  
        self.detected_frames_dir = detected_frames_dir 
        self.capture_range = 10
        self.is_running = True
        self.vehicle_process = {}
        self.vehicle_display_info = {}
        self.display_duration = 60
    



        
        if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
        if not os.path.exists(self.detected_frames_dir):
            os.makedirs(self.detected_frames_dir)
        

    async def process_video(self, input_source: str):
         if input_source.isdigit():
             self.camera_handler = CameraHandler(camera_id=int(input_source))
         elif os.path.exists(input_source):
             self.camera_handler = CameraHandler(camera_id=input_source)
         else:
             raise ValueError(f"Invalid input source: {input_source}")
         self.camera_handler.start_camera()

         try:
             while self.is_running:
                 frame = self.camera_handler.get_frame()
                 if frame is None:
                     break

                 preprocessed_frame, _, _ = await asyncio.get_running_loop().run_in_executor(None, preprocess_frame_func, frame)
                 async for height in self.process_frame(frame, preprocessed_frame):
                     pass
                
                 cv2.imshow('Vehicle Detection', frame)
                 if cv2.waitKey(1) & 0xFF == ord('q'):
                     self.stop_processing()
                     break
         finally:
             self.camera_handler.stop_camera()


    async def detect_and_track(self, frame) -> AsyncGenerator[int, None]:
        loop = asyncio.get_running_loop()
        frame = cv2.resize(frame, (900, 700))
        preprocessed_frame = await loop.run_in_executor(None, preprocess_frame_func, frame)
        startX, startY, endX, endY, center_coords = self._calculate_roi(frame)
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 255), 2)
        cv2.line(frame, center_coords[0], center_coords[1], (0, 255, 255), 2)
        async for height in self.process_frame(frame, preprocessed_frame):
            self.display_vehicle_info(frame)  
            cv2.imshow('Vehicle Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_processing()
            yield height 
        await self.process_frame(frame, preprocessed_frame)
        self.display_vehicle_info(frame)
        cv2.imshow('Vehicle Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.stop_processing()


    def stop_processing(self, camera_id=None):
        self.is_running = False
        if self.camera_handler:
            self.camera_handler.stop_camera()
            if camera_id and camera_id in active_camera_handlers:
                del active_camera_handlers[camera_id]
                


    async def process_frame(self, frame, preprocessed_frame):
        center_x = self._calculate_roi(frame)
        line_start_point = (center_x, 0)
        line_end_point = (center_x, frame.shape[0])
        cv2.line(frame, line_start_point, line_end_point, (0, 255, 255), 2)
        
        async for height in self._process_detections(frame, preprocessed_frame, center_x):
            yield height

       
    def _is_crossing_line(self, x, w, center_x):
        object_center = x + w // 2
        return abs(object_center - center_x) <= self.capture_range

    
    async def _process_detections(self, frame, preprocessed_frame, center_x):
        _, _, seg_contours, scores = self.segmentation_model.detect(preprocessed_frame)
        for seg, score in zip(seg_contours, scores):
            if score > self.confidence_threshold:
                x, y, w, h = cv2.boundingRect(seg)
                if self._is_crossing_line(x, w, center_x):
                    await self._process_detection_and_save(frame, seg, x, y, w, h, center_x)
                    truck_height_pixels = np.max(seg[:, 1]) - np.min(seg[:, 1])
                    truck_height_cm = int(truck_height_pixels / 1.65)
                    yield truck_height_cm

    
    async def _process_detection_and_save(self, frame, seg, x, y, w, h, center_x):
        cx = x + w // 2
        if abs(cx - center_x) <= self.capture_range:
            obj_id = hash(tuple(seg.flatten())) % 1e6
            if obj_id not in self.crossed_ids:
                self.crossed_ids.append(obj_id)
                truck_height_pixels = np.max(seg[:, 1]) - np.min(seg[:, 1])
                truck_height_cm = int(truck_height_pixels / 1.65)
                await frames_queue.put(truck_height_cm)
                cv2.putText(frame, f"Vehicle ID {obj_id}: Height {truck_height_cm} cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.drawContours(frame, [seg], -1, (0, 255, 0), 3)  # Draw in red with thickness of 3
                info_text = f"Vehicle ID {obj_id}: Height {truck_height_cm} cm"
                cv2.putText(frame, info_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                await self._save_snapshot_and_record(frame, obj_id, truck_height_cm)
                return truck_height_cm
                


    async def _save_snapshot_and_record(self, frame, obj_id, height_cm):
        snapshot_filename = os.path.join(self.snapped_folder, f'snapshot_{int(obj_id)}.jpg')
        cv2.imwrite(snapshot_filename, frame)
        new_vehicle = VehicleDetail(vehicle_id=str(obj_id), height=height_cm)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.db_session.add, new_vehicle)
        await loop.run_in_executor(None, self.db_session.commit)


    def _calculate_roi(self, frame):
        frame_height, frame_width = frame.shape[:2]
        center_x = frame_width // 2  # or set this to any other appropriate fixed value
        return center_x
    
    
    def display_vehicle_info(self, frame: np.ndarray):
        completed_vehicles = len(self.vehicle_process)
        cv2.putText(frame, f'Completed Vehicles: {completed_vehicles}', (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        for obj_id, info in list(self.vehicle_display_info.items()):
            if info['display_frame_count'] > 0:
                cv2.putText(frame, f'ID {obj_id}: Height {info["vertical_extent"]}', info['position'], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                info['display_frame_count'] -= 1
            else:
                del self.vehicle_display_info[obj_id]

    