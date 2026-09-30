import os
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import urllib.request

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ocr.paddle_ocr import get_ocr_service
from services.face.face_verification import get_face_service

def create_synthetic_doc(text, filename):
    # Create a white image
    img = Image.new('RGB', (800, 400), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    # Since we can't guarantee a font with Hindi/Marathi exists on Windows by default easily without
    # providing a path, we'll try to just use default or arial.
    # Note: On Windows, msgothic or nirmala supports devanagari
    try:
        font = ImageFont.truetype("nirmal.ttf", 32)
    except IOError:
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()
            
    d.text((50, 50), text, fill=(0, 0, 0), font=font)
    img.save(filename)

def test_ocr():
    print("--- OCR VALIDATION ---")
    ocr = get_ocr_service()
    
    docs = {
        "English": "Name: Rahul Sharma\nDOB: 15/08/1990\nAddress: 42, Main Road, Mumbai, Maharashtra",
        "Hindi": "नाम: राहुल शर्मा\nजन्म तिथि: १५/०८/१९९०\nपता: ४२, मुख्य मार्ग, मुंबई, महाराष्ट्र",
        "Marathi": "नाव: राहुल शर्मा\nजन्म तारीख: १५/०८/१९९०\nपत्ता: ४२, मुख्य रस्ता, मुंबई, महाराष्ट्र"
    }
    
    os.makedirs("datasets/test_images", exist_ok=True)
    
    for lang, text in docs.items():
        filename = f"datasets/test_images/doc_{lang}.jpg"
        create_synthetic_doc(text, filename)
        
        extracted = ocr.extract_text(filename)
        print(f"\n{lang} Extraction:")
        # Don't print direct Hindi/Marathi to console if it crashes, check length
        print(f"Extracted Length: {len(extracted)}")
        if "Rahul" in extracted or "राहुल" in extracted:
            print(f"Success: Name found in {lang} text.")
        else:
            print(f"Failed to find exact text in {lang} (maybe font issue).")

def download_image(url, filename):
    if not os.path.exists(filename):
        urllib.request.urlretrieve(url, filename)

def test_faces():
    print("\n--- FACE VALIDATION ---")
    face_svc = get_face_service()
    
    os.makedirs("datasets/test_images", exist_ok=True)
    
    # We use a standard test image (Lenna) - widely used and legally acceptable for testing
    img1_url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/lena.jpg"
    img1_path = "datasets/test_images/face1.jpg"
    download_image(img1_url, img1_path)
    
    # Create an image with NO face
    img_no_face = np.zeros((300, 300, 3), dtype=np.uint8)
    cv2.imwrite("datasets/test_images/no_face.jpg", img_no_face)
    
    # Same person
    res1 = face_svc.verify_faces(img1_path, img1_path)
    print("Same Person Match:", res1["decision"], "| Score:", res1.get("score", 0))
    
    # No face
    res2 = face_svc.verify_faces(img1_path, "datasets/test_images/no_face.jpg")
    print("No Face Detection:", res2["decision"])

if __name__ == "__main__":
    test_ocr()
    test_faces()
