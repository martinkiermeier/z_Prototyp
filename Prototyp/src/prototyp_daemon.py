from picamera2 import Picamera2
from PiCameraManager.CameraManager import CameraManager
from PersonRecognition.PersonRecognition import PersonRecognition
from LicensePlate.LicensePlateRecognition.LicensePlateRecognition import LicensePlateRecognition
from LicensePlate.LicensePlateOCR.LicensePlateOCR import LicensePlateOCR
from LIDAR_Manager.LIDAR_Manager import LIDAR_Manager
import time
import threading

def threads():
    thread_1 = threading.Thread(target=main_loop, args=(Camera_1,person_recognition,LIDAR_1))
    thread_2 = threading.Thread(target=main_loop, args=(Camera_2, person_recognition, LIDAR_2))
    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()

def main_loop(camera_manager,person_recognition,lidar):
    while True:
        ################################################################### /change to multiple photos
        #LIDAR + Camera (waits for LIDAR signal and captures frame)
        ###################################################################/add exceptions
        frame_c = None
        try:
            if lidar.vehicle_present():
                frame_c = camera_manager.capture_frame()
            else:
                time.sleep(0.1)
                continue
        except Exception as e:
            print(f"Worker Error: {e}")
            time.sleep(1)
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
        #save images...
        ###################################################################

        ###################################################################
        #wait if they charge or the LIDAR is reset
        ###################################################################
        for x in range (40):
            time.sleep(15)
            #test if charging started
            #test if LIDAR still active
                #has the LIDAR distance changed? Is it still the same plate?

        #if not charging: fine


Camera_1 = CameraManager(0)
Camera_2 = CameraManager(1)
LIDAR_1 = LIDAR_Manager("/dev/ttyUSB0")
LIDAR_2 = LIDAR_Manager("/dev/ttyUSB1")
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
LIDAR_1.calibrate()
LIDAR_2.calibrate()
threads()


Camera_1.stop()
Camera_2.stop()
Camera_1.close()
Camera_2.close()