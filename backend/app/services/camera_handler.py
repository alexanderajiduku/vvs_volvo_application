import cv2
import logging
from vmbpy import *
from app.services.undistortion_class import CameraFeedUndistorter

class CameraHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CameraHandler, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self, camera_id=0, output_path='output.avi', frame_width=1280, frame_height=720):
        if not self.initialized:
            self.camera_id = camera_id
            self.output_path = output_path
            self.frame_width = frame_width
            self.frame_height = frame_height
            self.cap = None
            self.vimba_system = VmbSystem.get_instance()
            self.undistorter = CameraFeedUndistorter()
            self.initialized = True
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def start_camera(self):
        with self.vimba_system as vimba:
            cameras = vimba.get_all_cameras()
            if not cameras or self.camera_id >= len(cameras):
                logging.error('No cameras found')
                return

            self.cap = cameras[self.camera_id]
            try:
                if self.cap.get_pixel_format() != PixelFormat.Mono8:
                    self.cap.set_pixel_format(PixelFormat.Bgr8)
            except Exception as e:
                logging.error("Error setting pixel format: {}".format(e))
                self.cap = None  

    def get_frame(self):
        if not self.cap:
            logging.error("Camera not initialized or camera capture method not found.")
            return None

        try:
            frame = self.cap.get_frame()
            if frame is None:
                logging.error("Failed to capture frame: No frame received.")
                return None

            img = frame.as_opencv_image()
            if img is None:
                logging.error("Failed to convert frame to OpenCV image.")
                return None

        except Exception as e:
            logging.error(f"Error during frame acquisition or conversion: {e}")
            return None

        try:
            undistorted_img = self.undistorter.undistort_frame(img)
            return undistorted_img
        except Exception as e:
            logging.error(f"Error undistorting frame: {e}")
            return None

    def stop_camera(self):
        if hasattr(self.cap, 'close'):
            try:
                self.cap.close()
                logging.info("Camera feed has been stopped.")
            except Exception as e:
                logging.error(f"Error during camera shutdown: {e}")
            finally:
                logging.info("All resources have been cleaned up.")

    def __del__(self):
        self.stop_camera()
