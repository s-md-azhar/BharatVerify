import cv2
import numpy as np
from paddleocr import PaddleOCR

def test_paddle():
    print("Initializing PaddleOCR...")
    ocr = PaddleOCR(use_textline_orientation=True, lang='en')
    
    print("Creating dummy image...")
    # Create a white image with some text
    img = np.ones((200, 400, 3), dtype=np.uint8) * 255
    cv2.putText(img, "JOHN DOE", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    print("Running OCR...")
    result = ocr.ocr(img, cls=True)
    print("Result:", result)
    if result and result[0]:
        print("Success! Detected:", [line[1][0] for line in result[0]])

if __name__ == "__main__":
    test_paddle()
