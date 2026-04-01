import cv2
import numpy as np
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

def run_ocr(image_bytes: bytes) -> list:
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    _, encoded = cv2.imencode('.png', thresh)
    result = reader.readtext(encoded.tobytes())
    lines = []
    for (bbox, text, confidence) in result:
        lines.append({
            "text": text,
            "confidence": round(confidence, 3),
            "bbox": [list(map(float, p)) for p in bbox]
        })
    return lines