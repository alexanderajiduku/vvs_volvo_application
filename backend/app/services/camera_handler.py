"""
import cv2
import logging
from vmbpy import VmbSystem, PixelFormat
 


class CameraHandler:

    _instance = None  
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CameraHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self, camera_id=1, output_path='output.avi', frame_width=1280, frame_height=720):
        if not hasattr(self, 'initialized'):
            self.camera_id = camera_id
            self.output_path = output_path
            self.frame_width = frame_width
            self.frame_height = frame_height
            self.cap = None 
            self.initialized = True
        

    def start_camera(self):
        try:
            with VmbSystem.get_instance() as vimba:
                cameras = vimba.get_all_cameras()
                if not cameras or self.camera_id >= len(cameras):
                    raise EnvironmentError('No suitable Allied Vision camera found.')
                camera = cameras[self.camera_id]
                camera.open()
                if camera.PixelFormat.get() != PixelFormat.Mono8:
                    camera.PixelFormat.set(PixelFormat.Bgr8)
                self.cap = camera

        except Exception as e:
            logging.info(f'Falling back to default camera due to an error or no Allied Vision camera available: {e}')
            self.cap = cv2.VideoCapture(self.camera_id)

            if not self.cap.isOpened():
                logging.error('Cannot open the default camera')
                raise IOError('Cannot open the default camera')

    def get_frame(self):
        if isinstance(self.cap, cv2.VideoCapture):
            ret, frame = self.cap.read()
            if ret:
                return frame
            else:
                logging.error("Can't receive frame (stream end?). Exiting ...")
                return None
        else:
            frame = self.cap.get_frame()  
            try:
                return frame.as_opencv_image()  
            except ValueError as e:
                logging.error(f"Error converting frame: {e}")
                return None

    def stop_camera(self):
        if self.cap:
            if isinstance(self.cap, cv2.VideoCapture):
                self.cap.release()
            else:
                self.cap.close()

            logging.info("Camera feed has been stopped.")
        """
import cv2
import logging
from vmbpy import VmbSystem, PixelFormat

class CameraHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CameraHandler, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self, camera_id=1, output_path='output.avi', frame_width=1280, frame_height=720):
        if not self.initialized:
            self.camera_id = camera_id
            self.output_path = output_path
            self.frame_width = frame_width
            self.frame_height = frame_height
            self.cap = None
            self.vimba_system = None
            self.initialized = True
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
                return frame
            else:
                logging.error("Can't receive frame (stream end?). Exiting ...")
                return None
        elif hasattr(self.cap, 'get_frame'):
            frame = self.cap.get_frame()
            try:
                return frame.as_opencv_image()
            except ValueError as e:
                logging.error(f"Error converting frame: {e}")
                return None
        else:
            logging.error("Camera capture method not found.")
            return None
    """
    def stop_camera(self):
        if isinstance(self.cap, cv2.VideoCapture):
            self.cap.release()
            cv2.destroyAllWindows()
        elif hasattr(self.cap, 'close'):
            self.cap.close()

        if self.vimba_system:
            self.vimba_system.shutdown()

        logging.info("Camera feed has been stopped.")
        cv2.destroyAllWindows()
    
    def stop_camera(self):
        if isinstance(self.cap, cv2.VideoCapture):
            self.cap.release()
            logging.info("OpenCV camera feed has been stopped.")
            cv2.destroyAllWindows()
        if hasattr(self.cap, 'close'):
            try:
                self.cap.close()
                logging.info("Allied Vision camera feed has been closed.")
            except Exception as e:
                logging.error(f"Failed to close Allied Vision camera: {e}")
        if self.vimba_system:
            try:
                shutdown_method = getattr(self.vimba_system, 'shutdown', None)
                if callable(shutdown_method):
                    shutdown_method()
                    logging.info("Vimba system shutdown successfully.")
                else:
                    logging.error("Vimba system does not support shutdown.")
            except Exception as e:
                logging.error(f"Error during Vimba system shutdown: {e}")
        cv2.destroyAllWindows()
     """ 
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