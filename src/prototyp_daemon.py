from picamera2 import Picamera2
from PiCameraManager.CameraManager import CameraManager
from PersonRecognition.PersonRecognition import PersonRecognition
from LicensePlate.LicensePlateRecognition.LicensePlateRecognition import LicensePlateRecognition
from LicensePlate.LicensePlateOCR.LicensePlateOCR import LicensePlateOCR
from LIDAR_Manager import LIDAR_Manager
import time

def main_loop(camera_manager1,camera_manager2,person_recognition, lidar_1,lidar_2):
    while True:
        ################################################################### /change to multiple photos
        #LIDAR + Camera (waits for LIDAR signal and captures frame)
        ###################################################################
        frame_c = None
        #multithreading?
        if lidar_1.vehicle_present():
            frame_c = camera_manager1.capture_frame()
        elif lidar_2.vehicle_present():
            frame_c = camera_manager2.capture_frame()
        else:
            continue
        ###################################################################
        #License Plate recognition
        ###################################################################
        recognized_plates = []
        plates = license_plate_recognition.detect_plates(frame_c)
        for x1, y1, x2, y2 in plates:
            plate_crop = (license_plate_recognition.crop_plate(frame_c,x1,y1,x2,y2))
            frame_c = (license_plate_recognition.draw_plate_frame(frame_c,x1,y1,x2,y2))
            plate_text = (license_plate_ocr.read_plate(plate_crop))
            recognized_plates.append({"text": plate_text,"crop": plate_crop,"bbox": (x1, y1, x2, y2)})

        ###################################################################
        #Person recognition
        ###################################################################
        img, scale, pad_x, pad_y = person_recognition.resize_picture_for_YOLOX_recognition(frame_c)
        persons = person_recognition.detect_person(img, scale, pad_x, pad_y)
        for person in persons:
            x1, y1, x2, y2 = person
            frame_c = person_recognition.pixelate_person(frame_c,x1,y1,x2,y2)
            frame_c = person_recognition.draw_person_frame(frame_c,x1,y1,x2,y2)
        ###################################################################
        #
        ###################################################################

Camera_1 = CameraManager(0)
Camera_2 = CameraManager(1)
LIDAR_1 = LIDAR_Manager(0)
LIDAR_2 = LIDAR_Manager(1)
LIDAR_1.calibrate()
LIDAR_2.calibrate()
license_plate_recognition = LicensePlateRecognition()
person_recognition = PersonRecognition()
license_plate_ocr = LicensePlateOCR()

print("Camera_1 start")
Camera_1.start()
print("Camera_2 start")
Camera_2.start()
print("LIDAR_1 start")
LIDAR_1.start()
print("LIDAR_2 start")
LIDAR_2.start()
main_loop(Camera_1, Camera_2, person_recognition, LIDAR_1, LIDAR_2)

Camera_1.stop()
Camera_2.stop()
Camera_1.close()
Camera_2.close()