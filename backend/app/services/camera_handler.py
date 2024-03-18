import cv2
import logging
from vmbpy import VmbSystem, PixelFormat
 
import cv2
import logging
from vmbpy import VmbSystem, PixelFormat

class CameraHandler:
    def __init__(self, camera_id=0, output_path='output.avi', frame_width=1280, frame_height=720):
        self.camera_id = camera_id
        self.output_path = output_path
        self.frame_width = frame_width
        self.frame_height = frame_height
 
    def get_camera_feed(self):
        try:
            with VmbSystem.get_instance() as vimba:
                cameras = vimba.get_all_cameras()
                if not cameras:
                    logging.info('No Allied Vision cameras found, trying default camera')
                    raise EnvironmentError('No Allied Vision cameras available')
 
                selected_camera = cameras[self.camera_id]
                if selected_camera.get_pixel_format() != PixelFormat.Mono8:
                    try:
                        selected_camera.set_pixel_format(PixelFormat.Bgr8)
                    except Exception as e:
                        logging.error(f"Error setting pixel format: {e}")
                        return
 
                while True:
                    frame = selected_camera.get_frame()
                    try:
                        yield frame.as_opencv_image()
                    except ValueError as e:
                        logging.error(f"Error converting frame: {e}")
                        return
 
        except Exception as e:
            logging.error(f"Switching to default camera due to an error: {e}")
            cap = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)
 
            if not cap.isOpened():
                logging.error('Cannot open default camera')
                return
 
            while True:
                ret, frame = cap.read()
                if not ret:
                    logging.error("Can't receive frame (stream end?). Exiting ...")
                    break
 
                yield frame
 
            cap.release()
