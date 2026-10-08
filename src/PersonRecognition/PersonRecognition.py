import torch
import cv2
import numpy as np
from yolox.exp import get_exp
from yolox.utils import postprocess

class PersonRecognition:
    def __init__(self,camera_id):
        
    def resize_picture_for_YOLOX_recognition(self,image):
        # ---------------------------------
        # Bild laden
        # ---------------------------------

        if image is None:
            print("Bild konnte nicht geladen werden")
            exit()

        print("Bild geladen:", image.shape)

        # Für YOLOX auf 640x640 skalieren

        new_width = 1280
        new_height = int(image.shape[0] * new_width / image.shape[1])
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

    def loadYOLOX(self):
        # ---------------------------------
        # YOLOX laden
        # ---------------------------------
        exp = get_exp(
            "/home/user/Sensor_Test_Rep/YOLOX/exps/default/yolox_nano.py",
            None
        )
        
        model = exp.get_model()
        
        ckpt = torch.load(
            "/home/user/Sensor_Test_Rep/models/yolox_nano.pth",
            map_location="cpu"
        )
        
        model.load_state_dict(ckpt["model"])
        
        model.eval()
        
        print("Modell bereit")
    def inferenz(self):
        with torch.no_grad():
            outputs = model(img)

        outputs = postprocess(
            outputs,
            num_classes=80,
            conf_thre=0.3,
            nms_thre=0.45
        )

        if outputs[0] is None:
            print("Keine Objekte gefunden")
            return[]

        
        
    