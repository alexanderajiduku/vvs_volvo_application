"""

import cv2
import numpy as np
import pandas as pd
import os 
from sqlalchemy.orm import Session
from app.models.model import Model
from .yolo_segmentation import YOLOSegmentation  
from app.models.vehicledetails import VehicleDetail
from .preprocessing import preprocess_frame_func
from app.utils.camera_utils import active_camera_handlers
from .undistortion_class import CameraFeedUndistorter
from app.shared.shared import frames_queue
from typing import AsyncGenerator
from fastapi import WebSocket
from vmbpy import *
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
        self.undistorter = CameraFeedUndistorter()
       
        
        if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
        if not os.path.exists(self.detected_frames_dir):
            os.makedirs(self.detected_frames_dir)
        

    async def process_video(self, input_source: str):
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
                    
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                video_out_path = os.path.join(self.output_dir, 'output_video.avi')
                out = cv2.VideoWriter(video_out_path, fourcc, 20.0, (1920, 1080))
            
                    
                try:
                    while self.is_running:
                        frame = cam.get_frame()
                        img = frame.as_opencv_image()
                        if img is None:
                            break

                        undistorted_frame = self.undistorter.undistort_frame(img)
                        preprocessed_frame, _, _ = await asyncio.get_running_loop().run_in_executor(None, preprocess_frame_func, undistorted_frame)
                        async for height in self.process_frame(undistorted_frame, preprocessed_frame):
                            pass

                        resized_frame = cv2.resize(undistorted_frame, (1200, 800))
                        cv2.imshow('Vehicle Detection', resized_frame)
                        out.write(undistorted_frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            self.stop_processing()
                            break
                finally:
                    out.release()


    async def detect_and_track(self, undistorted_frame) -> AsyncGenerator[int, None]:
        loop = asyncio.get_running_loop()
        frame = cv2.resize(undistorted, (1200, 800))
        preprocessed_frame = await loop.run_in_executor(None, preprocess_frame_func, undistorted_frame)
        startX, startY, endX, endY, center_coords = self._calculate_roi(undistorted_frame)
        cv2.rectangle(undistorted_frame, (startX, startY), (endX, endY), (0, 255, 255), 2)
        cv2.line(frame, center_coords[0], center_coords[1], (0, 255, 255), 2)
        async for height in self.process_frame(undistorted_frame, preprocessed_frame):
            self.display_vehicle_info(frame)  
            cv2.imshow('Vehicle Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_processing()
            yield height 
        await self.process_frame(undistorted_frame, preprocessed_frame)
         
                                                                                                                  
        self.display_vehicle_info(undistorted_frame)
        cv2.imshow('Vehicle Detection', undistorted_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.stop_processing()


    def stop_processing(self, camera_id=None):
        self.is_running = False
        if self.camera_handler:
            self.camera_handler.stop_camera()
            if camera_id and camera_id in active_camera_handlers:
                del active_camera_handlers[camera_id]
                


    async def process_frame(self, undistorted_frame, preprocessed_frame):
        center_x = self._calculate_roi(undistorted_frame)
        line_start_point = (center_x, 0)
        line_end_point = (center_x, undistorted_frame.shape[0])
        cv2.line(undistorted_frame, line_start_point, line_end_point, (0, 255, 255), 2)
        
        async for height in self._process_detections(undistorted_frame, preprocessed_frame, center_x):
            yield height

       
    def _is_crossing_line(self, x, w, center_x):
        object_center = x + w // 2
        return abs(object_center - center_x) <= self.capture_range

    
    async def _process_detections(self,  undistorted_frame, preprocessed_frame, center_x):
        _, _, seg_contours, scores = self.segmentation_model.detect(preprocessed_frame)
        for seg, score in zip(seg_contours, scores):
            if score > self.confidence_threshold:
                x, y, w, h = cv2.boundingRect(seg)
                if self._is_crossing_line(x, w, center_x):
                    await self._process_detection_and_save(undistorted_frame, seg, x, y, w, h, center_x)
                    truck_height_pixels = np.max(seg[:, 1]) - np.min(seg[:, 1])
                    truck_height_cm = int(truck_height_pixels / 1.65)
                    yield truck_height_cm

    
    async def _process_detection_and_save(self, undistorted_frame, seg, x, y, w, h, center_x):
        cx = x + w // 2
        if abs(cx - center_x) <= self.capture_range:
            obj_id = hash(tuple(seg.flatten())) % 1e6
            if obj_id not in self.crossed_ids:
                self.crossed_ids.append(obj_id)
                truck_height_pixels = np.max(seg[:, 1]) - np.min(seg[:, 1])
                truck_height_cm = int(truck_height_pixels / 1.65)
                await frames_queue.put(truck_height_cm)
                cv2.putText(undistorted_frame, f"Vehicle ID {obj_id}: Height {truck_height_cm} cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.drawContours( undistorted_frame, [seg], -1, (0, 255, 0), 3)  # Draw in red with thickness of 3
                info_text = f"Vehicle ID {obj_id}: Height {truck_height_cm} cm"
                cv2.putText(undistorted_frame, info_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                await self._save_snapshot_and_record(frame, obj_id, truck_height_cm)
                return truck_height_cm
                


    async def _save_snapshot_and_record(self, undistorted_frame, obj_id, height_cm):
        snapshot_filename = os.path.join(self.snapped_folder, f'snapshot_{int(obj_id)}.jpg')
        cv2.imwrite(snapshot_filename, undistorted_frame)
        new_vehicle = VehicleDetail(vehicle_id=str(obj_id), height=height_cm)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.db_session.add, new_vehicle)
        await loop.run_in_executor(None, self.db_session.commit)


    def _calculate_roi(self, undistorted_frame):
        frame_height, frame_width = undistorted_frame.shape[:2]
        center_x = frame_width // 2  # or set this to any other appropriate fixed value
        return center_x
    
    
    def display_vehicle_info(self, undistorted_frame: np.ndarray):
        completed_vehicles = len(self.vehicle_process)
        cv2.putText(undistorted_frame, f'Completed Vehicles: {completed_vehicles}', (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        for obj_id, info in list(self.vehicle_display_info.items()):
            if info['display_frame_count'] > 0:
                cv2.putText(undistorted_framee, f'ID {obj_id}: Height {info["vertical_extent"]}', info['position'], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                info['display_frame_count'] -= 1
            else:
                del self.vehicle_display_info[obj_id]
                
                
                
        """
"""      
import cv2
import numpy as np
import os 
from sqlalchemy.orm import Session
from app.models.model import Model
from .yolo_segmentation import YOLOSegmentation  
from app.models.vehicledetails import VehicleDetail
from .preprocessing import preprocess_frame_func
from app.utils.camera_utils import active_camera_handlers
from .undistortion_class import CameraFeedUndistorter
from app.shared.shared import frames_queue
from typing import AsyncGenerator
from fastapi import WebSocket
from vmbpy import *
import asyncio
import logging

class DetectionHandler:
    def __init__(self, model_id, db_session: Session, roi_settings, snapped_folder, confidence_threshold, capture_range, output_dir: str = 'processed_videos', detected_frames_dir: str = 'detected_frames'):
        self.model = db_session.query(Model).filter(Model.id == model_id).first()
        if self.model is None:
            raise ValueError(f"Model with ID {model_id} not found in the database")
        self.model_path = os.path.join('uploaded_models', self.model.filename)  
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"YOLO model file not found at {self.model_path}")
        
        self.db_session = db_session
        self.segmentation_model = YOLOSegmentation(self.model_path)
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
        self.undistorter = CameraFeedUndistorter()
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(self.detected_frames_dir):
            os.makedirs(self.detected_frames_dir)
        

    async def process_video(self, input_source: str):
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
                    
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                video_out_path = os.path.join(self.output_dir, 'output_video.avi')
                out = cv2.VideoWriter(video_out_path, fourcc, 20.0, (1920, 1080))
            
                try:
                    while self.is_running:
                        frame = cam.get_frame()
                        img = frame.as_opencv_image()
                        if img is None:
                            break

                        undistorted_frame = self.undistorter.undistort_frame(img)
                        preprocessed_frame, _, _ = await asyncio.get_running_loop().run_in_executor(None, preprocess_frame_func, undistorted_frame)
                        async for height in self.process_frame(undistorted_frame, preprocessed_frame):
                            pass

                        resized_frame = self.resize_frame(undistorted_frame)
                        cv2.imshow('Vehicle Detection', resized_frame)
                        out.write(undistorted_frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            self.stop_processing()
                            break
                finally:
                    out.release()


    async def detect_and_track(self, undistorted_frame) -> AsyncGenerator[int, None]:
        loop = asyncio.get_running_loop()
        frame = self.resize_frame(undistorted_frame)
        preprocessed_frame = await loop.run_in_executor(None, preprocess_frame_func, undistorted_frame)
        startX, startY, endX, endY, center_coords = self.calculate_roi(undistorted_frame)
        cv2.rectangle(undistorted_frame, (startX, startY), (endX, endY), (0, 255, 255), 2)
        cv2.line(frame, center_coords[0], center_coords[1], (0, 255, 255), 2)
        async for height in self.process_frame(undistorted_frame, preprocessed_frame):
            self.display_vehicle_info(frame)  
            cv2.imshow('Vehicle Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_processing()
            yield height 
        await self.process_frame(undistorted_frame, preprocessed_frame)
         
        self.display_vehicle_info(undistorted_frame)
        cv2.imshow('Vehicle Detection', undistorted_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.stop_processing()


    async def process_frame(self, undistorted_frame, preprocessed_frame):
        cv2.line(undistorted_frame, (self.line_x_position, 0), (self.line_x_position, undistorted_frame.shape[0]), (0, 255, 255), 2)
        async for height in self.process_detections(undistorted_frame, preprocessed_frame):
            yield height

       
    def is_crossing_line(self, x, w, center_x):
        object_center = x + w // 2
        return abs(object_center - center_x) <= self.capture_range

    
    async def process_detections(self, undistorted_frame, preprocessed_frame):
        _, _, seg_contours, scores = self.segmentation_model.detect(preprocessed_frame)
        for seg, score in zip(seg_contours, scores):
            if score > self.confidence_threshold:
                x, y, w, h = cv2.boundingRect(seg)
                min_x = np.min(seg[:, 0])
                max_x = np.max(seg[:, 0])
                if min_x <= self.line_x_position <= max_x:  # Check if the object crosses the fixed line
                    await self.process_detection_and_save(undistorted_frame, seg, x, y, w, h)
                    truck_height_pixels = np.max(seg[:, 1]) - np.min(seg[:, 1])
                    truck_height_cm = int(truck_height_pixels / 1.65)
                    yield truck_height_cm

    
    async def process_detection_and_save(self, undistorted_frame, seg, x, y, w, h, center_x):
        cx = x + w // 2
        if abs(cx - center_x) <= self.capture_range:
            obj_id = hash(tuple(seg.flatten())) % 1e6
            if obj_id not in self.crossed_ids:
                self.crossed_ids.append(obj_id)
                truck_height_pixels = np.max(seg[:, 1]) - np.min(seg[:, 1])
                truck_height_cm = int(truck_height_pixels / 1.65)
                await frames_queue.put(truck_height_cm)
                cv2.putText(undistorted_frame, f"Vehicle ID {obj_id}: Height {truck_height_cm} cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                cv2.drawContours( undistorted_frame, [seg], -1, (0, 255, 0), 3)  # Draw in red with thickness of 3
                info_text = f"Vehicle ID {obj_id}: Height {truck_height_cm} cm"
                cv2.putText(undistorted_frame, info_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                await self.save_snapshot_and_record(frame, obj_id, truck_height_cm)
                return truck_height_cm
                

    async def save_snapshot_and_record(self, undistorted_frame, obj_id, height_cm):
        snapshot_filename = os.path.join(self.snapped_folder, f'snapshot_{int(obj_id)}.jpg')
        cv2.imwrite(snapshot_filename, undistorted_frame)
        new_vehicle = VehicleDetail(vehicle_id=str(obj_id), height=height_cm)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.db_session.add, new_vehicle)
        await loop.run_in_executor(None, self.db_session.commit)


    def calculate_roi(self, undistorted_frame):
        frame_height, frame_width = undistorted_frame.shape[:2]
        center_x = frame_width // 2  # or set this to any other appropriate fixed value
        return center_x
    
    
    def resize_frame(self, frame):
        return cv2.resize(frame, (1200, 800))
    
    def display_vehicle_info(self, undistorted_frame: np.ndarray):
        completed_vehicles = len(self.vehicle_process)
        cv2.putText(undistorted_frame, f'Completed Vehicles: {completed_vehicles}', (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        for obj_id, info in list(self.vehicle_display_info.items()):
            if info['display_frame_count'] > 0:
                cv2.putText(undistorted_frame, f'ID {obj_id}: Height {info["vertical_extent"]}', info['position'], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                info['display_frame_count'] -= 1
            else:
                del self.vehicle_display_info[obj_id]

    def stop_processing(self, camera_id=None):
        self.is_running = False
        if self.camera_handler:
            self.camera_handler.stop_camera()
            if camera_id and camera_id in active_camera_handlers:
                del active_camera_handlers[camera_id]
                
                
                
        
        """  
"""       
import cv2
import numpy as np
import os
from sqlalchemy.orm import Session
from app.models.model import Model
from app.models.vehicledetails import VehicleDetail
from .yolo_segmentation import YOLOSegmentation
from .preprocessing import preprocess_frame_func
from app.shared.shared import frames_queue
from .undistortion_class import CameraFeedUndistorter
from vmbpy import VmbSystem, PixelFormat
import asyncio
import logging
import random
import string


class DetectionHandler:
    def __init__(self, model_id, db_session: Session, roi_settings, snapped_folder, confidence_threshold, capture_range, output_dir: str = 'processed_videos', detected_frames_dir: str = 'detected_frames', save_dir: str = 'snapshots'):
        self.model = db_session.query(Model).filter(Model.id == model_id).first()
        if self.model is None:
            raise ValueError(f"Model with ID {model_id} not found in the database")
        self.model_path = os.path.join('uploaded_models', self.model.filename)
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"YOLO model file not found at {self.model_path}")

        self.db_session = db_session
        self.segmentation_model = YOLOSegmentation(self.model_path)
        self.snapped_folder = snapped_folder
        self.confidence_threshold = confidence_threshold
        self.output_dir = output_dir
        self.detected_frames_dir = detected_frames_dir
        self.save_dir = save_dir
        self.snapshot_taken = False  
        self.is_running = True
        self.undistorter = CameraFeedUndistorter()

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(self.detected_frames_dir):
            os.makedirs(self.detected_frames_dir)
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        self.line_x_position = 750  

    async def process_video(self, input_source: str):
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

                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                video_out_path = os.path.join(self.output_dir, 'output_video.avi')
                out = cv2.VideoWriter(video_out_path, fourcc, 20.0, (1920, 1080))

                try:
                    while self.is_running:
                        frame = cam.get_frame()
                        img = frame.as_opencv_image()
                        if img is None:
                            break

                        undistorted_img = self.undistorter.undistort_frame(img)
                        _, _, seg_contours, scores = self.segmentation_model.detect(undistorted_img)
                        cv2.line(undistorted_img, (self.line_x_position, 0), (self.line_x_position, img.shape[0]), (255, 0, 0), 2)

                        for seg, score in zip(seg_contours, scores):
                            if score > 0.90 and not self.snapshot_taken:
                                await self.process_detection(undistorted_img, seg)

                        resized_frame = cv2.resize(undistorted_img, (1200, 800))
                        cv2.imshow('Vehicle Detection', resized_frame)
                        out.write(resized_frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            self.stop_processing()
                            break
                finally:
                    out.release()
                    cv2.destroyAllWindows()
                    
                    
    
    async def process_detection(self, undistorted_img, seg):
        min_x = np.min(seg[:, 0])
        max_x = np.max(seg[:, 0])
        
        if min_x <= self.line_x_position <= max_x:
            mask_height_pixels = np.max(seg[:, 1]) - np.min(seg[:, 1])
            pixel_to_cm_ratio = self.get_pixel_to_cm_ratio(mask_height_pixels)
            mask_height_cm = int(mask_height_pixels / pixel_to_cm_ratio)
            obj_id = self.generate_custom_id()  
            
            cv2.drawContours(undistorted_img, [seg], -1, (0, 255, 0), 2)
            cv2.putText(undistorted_img, f'Mask Height: {mask_height_cm:.2f} cm', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            await self.save_snapshot_and_record(undistorted_img, obj_id, mask_height_cm)

    async def save_snapshot_and_record(self, undistorted_frame, obj_id, mask_height_cm):
        snapshot_filename = os.path.join(self.snapped_folder, f'{obj_id}.jpg')
        cv2.imwrite(snapshot_filename, undistorted_frame)
        new_vehicle = VehicleDetail(vehicle_id=str(obj_id), height=mask_height_cm)
        self.db_session.add(new_vehicle)
        self.db_session.commit()
        await frames_queue.put(mask_height_cm)  
        
    def stop_processing(self):
        self.is_running = False  
                
 
    def get_pixel_to_cm_ratio(self, mask_height_pixels):
        ratio_dict = {
            (0, 1600): 4.7636,
            (1601, 1650): 4.91044,
            (1651, 1700): 4.92,
            (1701, 1750): 4.961,
            (1751, 1800): 4.866,
            (1801, 1850): 4.866,
            (1851, 1900): 4.8469,
            (1901, 1920): 4.882,
            (1921, 1950): 4.8019,
            (1951, float('inf')): 5  
        }

        for (start, end), ratio in ratio_dict.items():
            if start <= mask_height_pixels <= end:
                return ratio
        return 5  

    def generate_custom_id(self):
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        numbers = ''.join(random.choices(string.digits, k=5))
        return f"{letters}{numbers}"
    
    
    
""" 
"""

import cv2
import numpy as np
import os
from sqlalchemy.orm import Session
from app.models.model import Model
from app.models.vehicledetails import VehicleDetail
from .yolo_segmentation import YOLOSegmentation
from .preprocessing import preprocess_frame_func
from app.shared.shared import frames_queue
from .undistortion_class import CameraFeedUndistorter
from vmbpy import VmbSystem, PixelFormat
import asyncio
import logging
import random
import string


class DetectionHandler:
    def __init__(self, model_id, db_session: Session, roi_settings, snapped_folder, confidence_threshold, capture_range, output_dir: str = 'processed_videos', detected_frames_dir: str = 'detected_frames', save_dir: str = 'snapshots'):
        self.model = db_session.query(Model).filter(Model.id == model_id).first()
        if self.model is None:
            raise ValueError(f"Model with ID {model_id} not found in the database")
        self.model_path = os.path.join('uploaded_models', self.model.filename)
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"YOLO model file not found at {self.model_path}")

        self.db_session = db_session
        self.segmentation_model = YOLOSegmentation(self.model_path)
        self.snapped_folder = snapped_folder
        self.confidence_threshold = confidence_threshold
        self.output_dir = output_dir
        self.detected_frames_dir = detected_frames_dir
        self.save_dir = save_dir
        self.is_running = True
        self.undistorter = CameraFeedUndistorter()
        self.captured_objects = set()  # Set to track objects that have been captured

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(self.detected_frames_dir):
            os.makedirs(self.detected_frames_dir)
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        self.line_x_position = 750  

    async def process_video(self, input_source: str):
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

                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                video_out_path = os.path.join(self.output_dir, 'output_video.avi')
                out = cv2.VideoWriter(video_out_path, fourcc, 20.0, (1920, 1080))

                try:
                    while self.is_running:
                        frame = cam.get_frame()
                        img = frame.as_opencv_image()
                        if img is None:
                            break

                        undistorted_img = self.undistorter.undistort_frame(img)
                        _, _, seg_contours, scores = self.segmentation_model.detect(undistorted_img)
                        cv2.line(undistorted_img, (self.line_x_position, 0), (self.line_x_position, img.shape[0]), (255, 0, 0), 2)

                        for seg, score in zip(seg_contours, scores):
                            if score > 0.90:
                                await self.process_detection(undistorted_img, seg)

                        resized_frame = cv2.resize(undistorted_img, (1200, 800))
                        cv2.imshow('Vehicle Detection', resized_frame)
                        out.write(resized_frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            self.stop_processing()
                            break
                finally:
                    out.release()
                    cv2.destroyAllWindows()

    async def process_detection(self, undistorted_img, seg):
        min_x = np.min(seg[:, 0])
        max_x = np.max(seg[:, 0])
        obj_id = self.generate_custom_id()

        # Check if the bounding box crosses the line and if the object ID is new
        if min_x <= self.line_x_position <= max_x and obj_id not in self.captured_objects:
            mask_height_pixels = np.max(seg[:, 1]) - np.min(seg[:, 1])
            pixel_to_cm_ratio = self.get_pixel_to_cm_ratio(mask_height_pixels)
            mask_height_cm = int(mask_height_pixels / pixel_to_cm_ratio)

            cv2.drawContours(undistorted_img, [seg], -1, (0, 255, 0), 2)
            cv2.putText(undistorted_img, f'Mask Height: {mask_height_cm:.2f} cm', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            await self.save_snapshot_and_record(undistorted_img, obj_id, mask_height_cm)
            self.captured_objects.add(obj_id)

    async def save_snapshot_and_record(self, undistorted_frame, obj_id, mask_height_cm):
        snapshot_filename = os.path.join(self.snapped_folder, f'{obj_id}.jpg')
        cv2.imwrite(snapshot_filename, undistorted_frame)
        new_vehicle = VehicleDetail(vehicle_id=str(obj_id), height=mask_height_cm)
        self.db_session.add(new_vehicle)
        self.db_session.commit()
        await frames_queue.put(mask_height_cm)

    def stop_processing(self):
        self.is_running = False

    def get_pixel_to_cm_ratio(self, mask_height_pixels):
        ratio_dict = {
            (0, 1600): 4.7636,
            (1601, 1650): 4.91044,
            (1651, 1700): 4.92,
            (1701, 1750): 4.961,
            (1751, 1800): 4.866,
            (1801, 1850): 4.866,
            (1851, 1900): 4.8469,
            (1901, 1920): 4.882,
            (1921, 1950): 4.8019,
            (1951, float('inf')): 5
        }

        for (start, end), ratio in ratio_dict.items():
            if start <= mask_height_pixels <= end:
                return ratio
        return 5

    def generate_custom_id(self):
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        numbers = ''.join(random.choices(string.digits, k=5))
        return f"{letters}{numbers}"

"""


import cv2
import numpy as np
import os
from sqlalchemy.orm import Session
from app.models.model import Model
from app.models.vehicledetails import VehicleDetail
from .yolo_segmentation import YOLOSegmentation
from .preprocessing import preprocess_frame_func
from app.shared.shared import frames_queue
from .undistortion_class import CameraFeedUndistorter
from vmbpy import VmbSystem, PixelFormat
import asyncio
import logging
import random
import string


class DetectionHandler:
    def __init__(self, model_id, db_session: Session, roi_settings, snapped_folder, confidence_threshold, capture_range, output_dir: str = 'processed_videos', detected_frames_dir: str = 'detected_frames', save_dir: str = 'snapshots'):
        self.model = db_session.query(Model).filter(Model.id == model_id).first()
        if self.model is None:
            raise ValueError(f"Model with ID {model_id} not found in the database")
        self.model_path = os.path.join('uploaded_models', self.model.filename)
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"YOLO model file not found at {self.model_path}")

        self.db_session = db_session
        self.segmentation_model = YOLOSegmentation(self.model_path)
        self.snapped_folder = snapped_folder
        self.confidence_threshold = confidence_threshold
        self.output_dir = output_dir
        self.detected_frames_dir = detected_frames_dir
        self.save_dir = save_dir
        self.is_running = True
        self.undistorter = CameraFeedUndistorter()
        self.processed_objects = {}  # Track objects and their last known positions
        self.line_x_position = 750  
        self.line_x_position_2 = 2200 

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if not os.path.exists(self.detected_frames_dir):
            os.makedirs(self.detected_frames_dir)
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    async def process_video(self, input_source: str):
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

                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                video_out_path = os.path.join(self.output_dir, 'output_video.avi')
                out = cv2.VideoWriter(video_out_path, fourcc, 20.0, (1920, 1080))

                try:
                    while self.is_running:
                        frame = cam.get_frame()
                        img = frame.as_opencv_image()
                        if img is None:
                            break

                        undistorted_img = self.undistorter.undistort_frame(img)
                        _, _, seg_contours, scores = self.segmentation_model.detect(undistorted_img)
                        cv2.line(undistorted_img, (self.line_x_position, 0), (self.line_x_position, img.shape[0]), (0, 255, 0), 5)
                        cv2.line(undistorted_img, (self.line_x_position_2, 0), (self.line_x_position_2, img.shape[0]), (255, 255, 0), 5)

                        if await self.detect_and_process(undistorted_img, seg_contours, scores):
                            # Exit after capturing one frame
                            break

                        resized_frame = cv2.resize(undistorted_img, (1200, 800))
                        cv2.imshow('Vehicle Detection', resized_frame)
                        out.write(resized_frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            self.stop_processing()
                            break
                finally:
                    out.release()
                    cv2.destroyAllWindows()

    async def detect_and_process(self, undistorted_img, seg_contours, scores):
        for seg, score in zip(seg_contours, scores):
            if score > self.confidence_threshold:
                min_x = np.min(seg[:, 0])
                max_x = np.max(seg[:, 0])
                obj_id = f"{min_x}-{max_x}"

                if obj_id not in self.processed_objects:
                    # New object detected
                    if min_x <= self.line_x_position <= max_x:
                        self.processed_objects[obj_id] = "crossed"
                        await self.process_detection(undistorted_img, seg)
                        return True
                    else:
                        self.processed_objects[obj_id] = "not_crossed"
                elif self.processed_objects[obj_id] == "not_crossed" and min_x <= self.line_x_position <= max_x:
                    self.processed_objects[obj_id] = "crossed"
                    await self.process_detection(undistorted_img, seg)
                    
        self.processed_objects.clear()

    async def process_detection(self, undistorted_img, seg):
        mask_height_pixels = np.max(seg[:, 1]) - np.min(seg[:, 1])
        pixel_to_cm_ratio = self.get_pixel_to_cm_ratio(mask_height_pixels)
        mask_height_cm = int(mask_height_pixels / pixel_to_cm_ratio)
        obj_id = self.generate_custom_id()

        cv2.drawContours(undistorted_img, [seg], -1, (0, 255, 0), 2)
        cv2.putText(undistorted_img, f'Mask Height: {mask_height_cm:.2f} cm', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        await self.save_snapshot_and_record(undistorted_img, obj_id, mask_height_cm)

    async def save_snapshot_and_record(self, undistorted_frame, obj_id, mask_height_cm):
        snapshot_filename = os.path.join(self.snapped_folder, f'{obj_id}.jpg')
        cv2.imwrite(snapshot_filename, undistorted_frame)
        new_vehicle = VehicleDetail(vehicle_id=str(obj_id), height=mask_height_cm)
        self.db_session.add(new_vehicle)
        self.db_session.commit()
        await frames_queue.put(mask_height_cm)

    def stop_processing(self):
        self.is_running = False

    def get_pixel_to_cm_ratio(self, mask_height_pixels):
        ratio_dict = {
            (0, 1600): 4.7636,
            (1601, 1650): 4.91044,
            (1651, 1700): 4.92,
            (1701, 1750): 4.961,
            (1751, 1800): 4.866,
            (1801, 1850): 4.866,
            (1851, 1900): 4.8469,
            (1901, 1920): 4.882,
            (1921, 1950): 4.8019,
            (1951, float('inf')): 5
        }

        for (start, end), ratio in ratio_dict.items():
            if start <= mask_height_pixels <= end:
                return ratio
        return 5

    def generate_custom_id(self):
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        numbers = ''.join(random.choices(string.digits, k=5))
        return f"{letters}{numbers}"
        
        
