"""

import cv2
import logging
from vmbpy import *
from  app.services.undistortion_class import CameraFeedUndistorter


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
            self.vimba_system = None
            self.initialized = True
            self.undistorter = CameraFeedUndistorter()  
            logging.basicConfig(level=logging.INFO)

    def start_camera(self):
        try:
            self.vimba_system = VmbSystem.get_instance()
            cameras = self.vimba_system.get_all_cameras()
            if not cameras or self.camera_id >= len(cameras):
                raise EnvironmentError('No suitable Allied Vision camera found.')

            camera = cameras[self.camera_id]
            camera.open()
            if camera.PixelFormat.get() != PixelFormat.Mono8:
                camera.PixelFormat.set(PixelFormat.Bgr8)
            self.cap = camera

        except Exception as e:
            logging.warning(f'Falling back to default camera due to: {e}')
            self.cap = cv2.VideoCapture(self.camera_id)
            if not self.cap.isOpened():
                logging.error('Cannot open the default camera')
                raise IOError('Cannot open the default camera')

    def get_frame(self):
        if isinstance(self.cap, cv2.VideoCapture):
            ret, frame = self.cap.read()
            if ret:
                return self.undistorter.undistort_frame(frame)
            else:
                logging.error("Can't receive frame (stream end?). Exiting ...")
                return None
        elif hasattr(self.cap, 'get_frame'):
            frame = self.cap.get_frame()
            try:
                return self.undistorter.undistort_frame(frame.as_opencv_image())
            except ValueError as e:
                logging.error(f"Error converting frame: {e}")
                return None
        else:
            logging.error("Camera capture method not found.")
            return None

    def stop_camera(self):
        try:
            if isinstance(self.cap, cv2.VideoCapture):
                if self.cap.isOpened():
                    self.cap.release()
                    logging.info("OpenCV camera feed has been stopped.")
                    cv2.destroyAllWindows()
                else:
                    logging.info("OpenCV camera feed was already stopped or never started.")
            if hasattr(self.cap, 'close'):
                self.cap.close()
                logging.info("Allied Vision camera feed has been closed.")
            if self.vimba_system:
                shutdown_method = getattr(self.vimba_system, 'shutdown', None)
                if callable(shutdown_method):
                    shutdown_method()
                    logging.info("Vimba system shutdown successfully.")
                else:
                    logging.error("Vimba system does not support shutdown.")
        except Exception as e:
            logging.error(f"Error during camera or system shutdown: {e}")
        finally:
            cv2.destroyAllWindows()
            logging.info("All camera feeds and resources have been cleaned up.")
    
     
    def __del__(self):
        self.stop_camera()
        
        
"""   
import cv2
import logging
from vmbpy import VmbSystem, PixelFormat
from app.services.undistortion_class import CameraFeedUndistorter

# Global variables to maintain state
camera_id = 0
output_path = 'output.avi'
frame_width = 1280
frame_height = 720
cap = None
vimba_system = None
undistorter = CameraFeedUndistorter()
initialized = False

# Initialize logging
logging.basicConfig(level=logging.INFO)

def initialize_camera(camera_id_param=0, output_path_param='output.avi', frame_width_param=1280, frame_height_param=720):
    global camera_id, output_path, frame_width, frame_height, initialized
    if not initialized:
        camera_id = camera_id_param
        output_path = output_path_param
        frame_width = frame_width_param
        frame_height = frame_height_param
        initialized = True

def start_camera():
    global vimba_system, cap
    try:
        vimba_system = VmbSystem.get_instance()
        cameras = vimba_system.get_all_cameras()
        if not cameras or camera_id >= len(cameras):
            raise EnvironmentError('No suitable Allied Vision camera found.')

        camera = cameras[camera_id]
        camera.open()
        if camera.PixelFormat.get() != PixelFormat.Mono8:
            camera.PixelFormat.set(PixelFormat.Bgr8)
        cap = camera

    except Exception as e:
        logging.warning(f'Falling back to default camera due to: {e}')
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            logging.error('Cannot open the default camera')
            raise IOError('Cannot open the default camera')

def get_frame():
    if isinstance(cap, cv2.VideoCapture):
        ret, frame = cap.read()
        if ret:
            return undistorter.undistort_frame(frame)
        else:
            logging.error("Can't receive frame (stream end?). Exiting ...")
            return None
    elif hasattr(cap, 'get_frame'):
        frame = cap.get_frame()
        try:
            return undistorter.undistort_frame(frame.as_opencv_image())
        except ValueError as e:
            logging.error(f"Error converting frame: {e}")
            return None
    else:
        logging.error("Camera capture method not found.")
        return None

def stop_camera():
    global vimba_system, cap
    try:
        if isinstance(cap, cv2.VideoCapture):
            if cap.isOpened():
                cap.release()
                logging.info("OpenCV camera feed has been stopped.")
            else:
                logging.info("OpenCV camera feed was already stopped or never started.")
        if hasattr(cap, 'close'):
            cap.close()
            logging.info("Allied Vision camera feed has been closed.")
        if vimba_system:
            shutdown_method = getattr(vimba_system, 'shutdown', None)
            if callable(shutdown_method):
                shutdown_method()
                logging.info("Vimba system shutdown successfully.")
            else:
                logging.error("Vimba system does not support shutdown.")
    except Exception as e:
        logging.error(f"Error during camera or system shutdown: {e}")
    finally:
        cv2.destroyAllWindows()
        logging.info("All camera feeds and resources have been cleaned up.")

def clean_up():
    stop_camera()

