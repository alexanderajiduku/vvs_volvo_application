# services/yolo_segmentation.py

import numpy as np
from ultralytics import YOLO
import logging

class YOLOSegmentation:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, img):
        height, width, _ = img.shape
        results = self.model.predict(source=img.copy(), save=False, save_txt=False)
        result = results[0]

        segmentation_contours_idx = []
        masks = getattr(result.masks, 'xyn', None)
        if masks is not None:
            for seg in masks:
                seg[:, 0] *= width
                seg[:, 1] *= height
                segment = np.array(seg, dtype=np.int32)
                segmentation_contours_idx.append(segment)
        if hasattr(result.boxes, 'xyxy') and hasattr(result.boxes, 'cls') and hasattr(result.boxes, 'conf'):
            bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
            class_ids = np.array(result.boxes.cls.cpu(), dtype="int")
            scores = np.array(result.boxes.conf.cpu(), dtype="float").round(2)
        else:
            logging.warning("Detection results do not contain expected attributes.")
            bboxes, class_ids, scores = np.array([]), np.array([]), np.array([])

        return bboxes, class_ids, segmentation_contours_idx, scores
