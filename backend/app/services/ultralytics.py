from ultralytics import YOLO
import cv2
from ultralytics.utils.plotting import Annotator  
import os
from typing import Dict, Any
import logging
from app.database.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.models.annotatedfiles import AnnotatedFile
from app.models.model import Model

logger = logging.getLogger(__name__)

class YOLOService:
    """
    A class that provides services for predicting and annotating images and videos using YOLO models.

    Args:
        model_id (int): The ID of the YOLO model to use for predictions.
        db_session (Session): The database session object.

    Attributes:
        yolo_model (YOLO): The YOLO model object.
        annotated_dir (str): The directory path for storing annotated results.

    Methods:
        predict_and_annotate_image: Predicts and annotates an image.
        predict_and_annotate_video: Predicts and annotates a video.
    """

    def __init__(self, model_id: int, db_session: Session):
        model = db_session.query(Model).filter(Model.id == model_id).first()
        if model is None:
            raise ValueError(f"Model with ID {model_id} not found in the database")
        model_path = os.path.join('uploaded_models', model.filename)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"YOLO model file not found at {model_path}")
        self.yolo_model = YOLO(model_path)

        self.annotated_dir = os.path.join(os.getcwd(), 'annotated_results')
        os.makedirs(self.annotated_dir, exist_ok=True)

    def predict_and_annotate_image(self, img_path: str) -> Dict[str, Any]:
        """
        Predicts and annotates an image.

        Args:
            img_path (str): The path to the input image.

        Returns:
            dict: A dictionary containing the original filename, annotated filename, and annotated filepath.
        """
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Could not read the image from {img_path}")
        results = self.yolo_model.predict(img)
        annotator = Annotator(img)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]
                c = box.cls
                annotator.box_label(b, self.yolo_model.names[int(c)])
        annotated_img = annotator.result()
        annotated_img_filename = os.path.basename(img_path).rsplit('.', 1)[0] + '_annotated.jpg'
        annotated_img_path = os.path.join(self.annotated_dir, annotated_img_filename)
        cv2.imwrite(annotated_img_path, annotated_img)
        return {
            "original_filename": os.path.basename(img_path),
            "annotated_filename": annotated_img_filename,
            "annotated_filepath": annotated_img_path
        }

    def predict_and_annotate_video(self, video_path: str) -> Dict[str, Any]:
        """
        Predicts and annotates a video.

        Args:
            video_path (str): The path to the input video.

        Returns:
            dict: A dictionary containing the original filename, annotated filename, and annotated filepath.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error(f"Could not open video {video_path}")
            return {"error": "Could not open video"}

        frame_width, frame_height = int(cap.get(3)), int(cap.get(4))
        annotated_video_filename = os.path.basename(video_path).rsplit('.', 1)[0] + '_annotated.mp4'
        annotated_video_path = os.path.join(self.annotated_dir, annotated_video_filename)
        out = cv2.VideoWriter(annotated_video_path, cv2.VideoWriter_fourcc(*'MP4V'), 30, (frame_width, frame_height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                logger.info("Reached end of video or error reading frame")
                break

            results = self.yolo_model.predict(frame)
            annotator = Annotator(frame)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]
                    c = box.cls
                    annotator.box_label(b, self.yolo_model.names[int(c)])

            annotated_frame = annotator.result()
            out.write(annotated_frame)
            logger.debug("Wrote annotated frame")

        cap.release()
        out.release()
        logger.info("Finished processing video")
        return {
            "original_filename": os.path.basename(video_path),
            "annotated_filename": annotated_video_filename,
            "annotated_filepath": annotated_video_path
        }
