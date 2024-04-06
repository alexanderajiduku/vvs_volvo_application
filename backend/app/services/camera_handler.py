import cv2
import logging
from vmbpy import VmbSystem, PixelFormat
 


class CameraHandler:
    def __init__(self, camera_id=1, output_path='output.avi', frame_width=1280, frame_height=720):
        self.camera_id = camera_id
        self.output_path = output_path
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.cap = None 
        

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