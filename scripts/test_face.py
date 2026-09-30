import os
import cv2
import numpy as np
from services.face.face_verification import get_face_service

def test_face():
    print("Testing face matching...")
    service = get_face_service()
    
    # Create two dummy images with face-like structures
    img1 = np.ones((300, 300, 3), dtype=np.uint8) * 200
    cv2.circle(img1, (150, 150), 50, (0, 0, 0), -1) # "Face"
    
    img2 = np.ones((300, 300, 3), dtype=np.uint8) * 200
    cv2.circle(img2, (150, 150), 50, (0, 0, 0), -1) # "Face"
    
    cv2.imwrite("dummy_face1.jpg", img1)
    cv2.imwrite("dummy_face2.jpg", img2)
    
    try:
        result = service.verify_faces("dummy_face1.jpg", "dummy_face2.jpg")
        print("Face result:", result)
    except Exception as e:
        print("Error during face matching:", e)
    finally:
        if os.path.exists("dummy_face1.jpg"):
            os.remove("dummy_face1.jpg")
        if os.path.exists("dummy_face2.jpg"):
            os.remove("dummy_face2.jpg")

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    test_face()
