import os
import sys
import cv2
import numpy as np
import urllib.request
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.face.face_verification import get_face_service

def create_no_face_img(path):
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    cv2.imwrite(path, img)

def download_img(url, path):
    if not os.path.exists(path):
        urllib.request.urlretrieve(url, path)

def run_face_benchmark():
    os.makedirs("datasets/test_faces", exist_ok=True)
    
    # 1. Same person (Lena)
    lena_url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/lena.jpg"
    lena_path = "datasets/test_faces/lena.jpg"
    download_img(lena_url, lena_path)
    
    # 2. Different person (Baboon - no face, or maybe another OpenCV sample image)
    # Let's get an actual face from OpenCV samples: messi5.jpg
    messi_url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/messi5.jpg"
    messi_path = "datasets/test_faces/messi.jpg"
    download_img(messi_url, messi_path)
    
    # 3. No face
    no_face_path = "datasets/test_faces/no_face.jpg"
    create_no_face_img(no_face_path)
    
    # 4. Multiple faces (OpenCV group of people or just stick messi and lena together)
    img1 = cv2.imread(lena_path)
    img2 = cv2.imread(messi_path)
    img1_resized = cv2.resize(img1, (300, 300))
    img2_resized = cv2.resize(img2, (300, 300))
    multi_face = np.hstack((img1_resized, img2_resized))
    multi_face_path = "datasets/test_faces/multi.jpg"
    cv2.imwrite(multi_face_path, multi_face)

    face_svc = get_face_service()

    print("--- FACE VERIFICATION BENCHMARK ---")
    
    # Same Person
    res1 = face_svc.verify_faces(lena_path, lena_path)
    print(f"Same Person: {res1['decision']} | Sim: {res1.get('similarity', 0):.4f}")
    
    # Different Person
    res2 = face_svc.verify_faces(lena_path, messi_path)
    print(f"Different Person: {res2['decision']} | Sim: {res2.get('similarity', 0):.4f}")
    
    # No Face
    res3 = face_svc.verify_faces(lena_path, no_face_path)
    print(f"No Face: {res3['decision']} | Found: {res3['face_found']}")
    
    # Multiple Faces against single
    # YuNet detects all, we pick largest. The output will be one face matched against Lena
    res4 = face_svc.verify_faces(lena_path, multi_face_path)
    print(f"Multiple Faces: {res4['decision']} | Found: {res4['face_found']} | Sim: {res4.get('similarity', 0):.4f}")

if __name__ == "__main__":
    run_face_benchmark()
