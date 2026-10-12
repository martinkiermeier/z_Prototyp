from fast_plate_ocr import ONNXPlateRecognizer

class LicensePlateOCR:
    def __init__(self):
        self.ocr_model = ONNXPlateRecognizer("european-plates-mobile-vit-v2-model")
        print("OCR ready")
    def read(self, plate_crop):
        try:
            text = self.ocr_model.run(plate_crop)
            if isinstance(text, list):
                text = text[0]
            return text

        except Exception as e:
            print("OCR error:", e)
            return None