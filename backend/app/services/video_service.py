import cv2
import signal
import sys
from threading import Thread

class VideoService:
 
    def __init__(self, camera_id: int):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(camera_id)
        self.ret = False
        self.frame = None
        if not self.cap.isOpened():
            raise ValueError("Unable to open camera")
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            self.ret, self.frame = self.cap.read()
            if not self.ret:
                print("Failed to grab frame")
                break

    def stream_video(self, *args):
        while True:
            if not self.ret:
                break
            flag, encodedImage = cv2.imencode(".jpg", self.frame)
            if not flag:
                continue
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

    @staticmethod
    def signal_handler(sig, frame):
        print('You pressed Ctrl+C! Stopping the video stream...')
        sys.exit(0)

    def display_video(self):
        while True:
            if not self.ret:
                print("Failed to grab frame")
                break
            cv2.imshow('Live Video', self.frame)
            
            # 'q' to quit the window
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    
        self.cap.release()
        cv2.destroyAllWindows()

# Usage
if __name__ == "__main__":
    camera_id = 1  
    video_service = VideoService(camera_id)
    signal.signal(signal.SIGINT, video_service.signal_handler) 
    video_service.display_video()
