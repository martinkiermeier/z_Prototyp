from picamera2 import Picamera2
from PiCameraManager.CameraManager import CameraManager
from PersonRecognition.PersonRecognition import PersonRecognition
from LicensePlate.LicensePlateRecognition.LicensePlateRecognition import LicensePlateRecognition
import time

def main_loop(camera_manager1,camera_manager2,person_recognition):
    while True:
        ###################################################################
        #Camera
        ###################################################################
        frame_c = None
        LIDARSIGNAL = input("1 für LIDAR1; 2 für LIDAR2: ")#multithreading?
        if LIDARSIGNAL=="1":
            frame_c =camera_manager1.capture_frame()
        elif LIDARSIGNAL=="2":
            frame_c = camera_manager2.capture_frame()
        else:
            print("LIDAR signal not recognized")
            continue
        ###################################################################
        #License Plate recognition
        ###################################################################
        plate_crops = []
        plates = LicensePlateRecognition.detect_plates(frame_c)
        for plate in plates:
            x1, y1, x2, y2 = plate
            plate_crops.append(license_plate_recognition.crop_plate(frame_c,x1,y1,x2,y2))
            frame_c = license_plate_recognition.draw_plate_frame()
        ###################################################################
        #OCR License Plate recognition
        ###################################################################

        ###################################################################
        #Person recognition
        ###################################################################
        img, scale, pad_x, pad_y = person_recognition.resize_picture_for_YOLOX_recognition(frame_c)
        persons = person_recognition.person_recognition(img, scale, pad_x, pad_y)
        for person in persons:
            x1, y1, x2, y2 = person
            frame_c = person_recognition.pixelate_person(frame_c,x1,y1,x2,y2)
            frame_c = person_recognition.draw_person_frame(frame_c,x1,y1,x2,y2)

Camera_1 = CameraManager(0)
Camera_2 = CameraManager(1)
license_plate_recognition = LicensePlateRecognition()
person_recognition = PersonRecognition()

print("Camera_1 start")
Camera_1.start()
print("Camera_2 start")
Camera_2.start()

main_loop(Camera_1, Camera_2, person_recognition)

Camera_1.stop()
Camera_2.stop()
Camera_1.close()
Camera_2.close()