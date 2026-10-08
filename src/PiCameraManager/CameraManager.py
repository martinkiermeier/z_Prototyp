from picamera2 import Picamera2
import time
class CameraManager:
    def __init__(self,camera_id):
        self.camera_id=camera_id
        self.picam2 = Picamera2(camera_id)
        print("picam2 init")
    def start(self):
        self.picam2.start()
        print("setup wait(1/3)")
        time.sleep(1)
        print("setup wait(2/3)")
        time.sleep(1)
        print("setup wait(3/3)")
        
    def stop(self):
        self.picam2.stop()
        print("picam2 stoped")
    def close(self):
        self.picam2.close()
        print("picam2 closed")
    def capture_frame(self):
        print("capture frame")
        frame = self.picam2.capture_array()
        return frame
    def capture_and_save_frame(self):
        self.picam2.capture_file("foto.jpg")
        print("capture and save frame")