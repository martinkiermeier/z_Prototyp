from fast_plate_ocr import LicensePlateRecognizer

class LicensePlateOCR:
    def __init__(self):
        self.ocr_model = LicensePlateRecognizer("european-plates-mobile-vit-v2-model")
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
#
#models = [
#    "european-plates-mobile-vit-v2-model",
#    "cct-xs-v2-global-model",
#    "cct-s-v2-global-model"
#]