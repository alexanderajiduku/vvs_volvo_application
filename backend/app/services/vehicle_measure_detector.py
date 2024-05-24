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
        (0, 1500): 5,
        (1501, 1550): 4.95911,
        (1551, 1600): 4.8940,
        (1601, 1650): 4.88059,
        (1651, 1700): 4.92,
        (1701, 1750): 4.961,
        (1751, 1800): 4.866,
        (1801, 1850): 4.866,
        (1851, 1900): 4.8010,
        (1901, 1920): 4.882,
        (1921, 1950): 4.8019,
        (1951, float('inf')): 5.165
    }

        for (start, end), ratio in ratio_dict.items():
            if start <= mask_height_pixels <= end:
                return ratio
        return 5

    def generate_custom_id(self):
        letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        numbers = ''.join(random.choices(string.digits, k=5))
        return f"{letters}{numbers}"
        
        
