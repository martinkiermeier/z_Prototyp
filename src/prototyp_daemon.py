from picamera2 import Picamera2
from PiCameraManager.CameraManager import CameraManager
from PersonRecognition.PersonRecognition import PersonRecognition
import time

def main_loop(camera_manager1,camera_manager2):
    while True:
        LIDARSIGNAL = input("1 für LIDAR1; 2 für LIDAR2: ")#multithreading?
        if LIDARSIGNAL=="1":
            frame_c1 =camera_manager1.capture_and_save_frame()
        if LIDARSIGNAL=="2":
            frame_c2 = camera_manager2.capture_and_save_frame()


Camera_1 = CameraManager(0)
Camera_2 = CameraManager(1)

Person_Recognition = PersonRecognition()

print("Camera_1 start")
Camera_1.start()
print("Camera_2 start")
Camera_2.start()

main_loop(Camera_1,Camera_2)

Camera_1.stop()
Camera_2.stop()
Camera_1.close()
Camera_2.close()