import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))#"/home/user/z_Prototyp/Prototyp/src/
import sys
#sys.path.append("/home/user/z_Prototyp/src/YOLOX")
import torch
import cv2
from yolox.exp import get_exp
from yolox.data.data_augment import ValTransform
from yolox.utils import postprocess

class LicensePlateRecognition:
    def __init__(self):
        #self.exp = get_exp("/home/user/z_Prototyp/src/YOLOX/exps/default/yolox_s.py")#change later
        self.exp = get_exp(
            os.path.join(BASE_DIR,"YOLOX", "exps","default","yolox_s.py"#change later
            ),None
        )
        self.exp.num_classes = 3
        self.model = self.exp.get_model()
        #ckpt = torch.load("/home/user/z_Prototyp/models/latest_ckpt.pth",map_location="cpu",weights_only=False)#change later
        ckpt = torch.load(
            os.path.join(BASE_DIR,"..","models","latest_ckpt.pth"),#change later
            map_location="cpu",weights_only=False
        )
        self.model.load_state_dict(ckpt["model"])
        self.model.eval()

    def detect_plates(self, frame):
        plates = []
        ratio = min(
            self.exp.test_size[0] / frame.shape[0],
            self.exp.test_size[1] / frame.shape[1]
        )
        preproc = ValTransform(legacy=False)
        img_input, _ = preproc(frame, None, self.exp.test_size)
        img_input = (torch.from_numpy(img_input).unsqueeze(0).float())
        with torch.no_grad():
            outputs = self.model(img_input)
            outputs = postprocess(outputs,self.exp.num_classes,conf_thre=0.25,nms_thre=0.45,class_agnostic=True)
        if outputs[0] is None:
            return []
        output = outputs[0]
        bboxes = output[:, 0:4]
        bboxes /= ratio
        for box in bboxes:
            x1, y1, x2, y2 = map(int,box)
            plates.append((x1, y1, x2, y2))
            print("Kennzeichen:",x1,y1,x2,y2)
        return plates

    def crop_plate(self, frame, x1, y1, x2, y2):
        width = x2 - x1
        height = y2 - y1
        margin_x = int(width * 0.15)
        margin_y = int(height * 0.30)
        x1_crop = max(0,x1 - margin_x)
        y1_crop = max(0,y1 - margin_y)
        x2_crop = min(frame.shape[1],x2 + margin_x)
        y2_crop = min(frame.shape[0],y2 + margin_y)
        plate_crop = frame[y1_crop:y2_crop,x1_crop:x2_crop]
        return plate_crop

    def draw_plate_frame(self,frame,x1,y1,x2,y2):
        cv2.rectangle(frame,(x1, y1),(x2, y2),(0, 255, 0),3)
        return frame