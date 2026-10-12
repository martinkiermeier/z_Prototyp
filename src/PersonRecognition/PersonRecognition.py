import torch
import cv2
import numpy as np
from yolox.exp import get_exp
from yolox.utils import postprocess

class PersonRecognition:
    def __init__(self):
        # ---------------------------------
        # YOLOX laden
        # ---------------------------------
        exp = get_exp(
            "/home/user/Sensor_Test_Rep/YOLOX/exps/default/yolox_nano.py",
            None
        )
        
        self.model = exp.get_model()
        
        ckpt = torch.load(
            "/home/user/Sensor_Test_Rep/models/yolox_nano.pth",
            map_location="cpu"
        )
        
        self.model.load_state_dict(ckpt["model"])
        
        self.model.eval()
        print("Modell bereit")

    def resize_picture_for_YOLOX_recognition(self,image):
        # ---------------------------------
        # Bild laden
        # ---------------------------------

        if image is None:
            print("Bild konnte nicht geladen werden")
            exit()

        print("Bild geladen:", image.shape)

        # Für YOLOX auf 640x640 skalieren

        target_size = 1280

        h, w = image.shape[:2]

        scale = target_size / max(w, h)

        new_w = int(w * scale)
        new_h = int(h * scale)
        resized = cv2.resize(
            image,
            (new_w, new_h)
        )
        letterbox = np.zeros(
            (target_size, target_size, 3),
            dtype=np.uint8
        )

        pad_x = (target_size - new_w) // 2
        pad_y = (target_size - new_h) // 2

        letterbox[
            pad_y:pad_y + new_h,
            pad_x:pad_x + new_w
        ] = resized

        small = letterbox

        print("YOLO Bildgröße:", small.shape)
        img = torch.from_numpy(small).float()
        img = img.permute(2, 0, 1)
        img = img.unsqueeze(0)

        return img, scale, pad_x, pad_y
        
    def person_recognition(self, img, scale, pad_x, pad_y):
        
        persons = []
        
        with torch.no_grad():
            outputs = self.model(img)

        outputs = postprocess(
            outputs,
            num_classes=80,
            conf_thre=0.3,
            nms_thre=0.45
        )

        if outputs[0] is None:
            print("Keine Objekte gefunden")
            return[]
    
        # ---------------------------------
        # Personen erkennen
        # ---------------------------------
        detections = outputs[0]
        for det in detections:
            cls = int(det[6])
            # Klasse 0 = Person
            if cls != 0:
                continue

            x1 = int((det[0] - pad_x) / scale)
            y1 = int((det[1] - pad_y) / scale)

            x2 = int((det[2] - pad_x) / scale)
            y2 = int((det[3] - pad_y) / scale)
            persons.append((x1, y1, x2, y2))
            print(
                "Person gefunden:",
                x1,
                y1,
                x2,
                y2
            )
        return persons
    def pixelate_person(self, image, x1, y1, x2, y2):
     
        # Größe des Originalbildes bestimmen
        h, w = image.shape[:2]
         
        # Koordinaten auf die Bildgrenzen begrenzen
        x1 = max(0, min(x1, w))
        x2 = max(0, min(x2, w))
        y1 = max(0, min(y1, h))
        y2 = max(0, min(y2, h))
         
        # Person aus dem Bild ausschneiden
        person = image[y1:y2, x1:x2]
         
        if person.size > 0:
             
            pixelated = cv2.resize(
                person,
                (20, 20),
                interpolation=cv2.INTER_LINEAR
            )
             
            pixelated = cv2.resize(
                pixelated,
                (x2 - x1, y2 - y1),
                interpolation=cv2.INTER_NEAREST
            )
             
            image[y1:y2, x1:x2] = pixelated
         
        return image

    def draw_person_frame(self, image, x1, y1, x2, y2):
            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                3
            )
            return image
