import os
import cv2
import numpy as np
import urllib.request

class FaceVerificationService:
    _instance = None
    
    YUNET_URL = "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"
    SFACE_URL = "https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx"
    
    def __init__(self, models_dir="model_artifacts"):
        self.models_dir = models_dir
        os.makedirs(self.models_dir, exist_ok=True)
        self.yunet_path = os.path.join(self.models_dir, "face_detection_yunet_2023mar.onnx")
        self.sface_path = os.path.join(self.models_dir, "face_recognition_sface_2021dec.onnx")
        
        self._ensure_models_downloaded()
        
        self.detector = cv2.FaceDetectorYN.create(self.yunet_path, "", (320, 320), 0.9, 0.3, 5000)
        self.recognizer = cv2.FaceRecognizerSF.create(self.sface_path, "")

    def _ensure_models_downloaded(self):
        if not os.path.exists(self.yunet_path):
            print("Downloading YuNet model...")
            urllib.request.urlretrieve(self.YUNET_URL, self.yunet_path)
        if not os.path.exists(self.sface_path):
            print("Downloading SFace model...")
            urllib.request.urlretrieve(self.SFACE_URL, self.sface_path)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _detect_face(self, image: np.ndarray):
        height, width, _ = image.shape
        self.detector.setInputSize((width, height))
        _, faces = self.detector.detect(image)
        return faces

    def verify_faces(self, img1_path: str, img2_path: str) -> dict:
        """Verifies if two face images belong to the same person."""
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)
        
        if img1 is None or img2 is None:
            return {"face_found": False, "similarity": 0.0, "decision": "ERROR"}

        faces1 = self._detect_face(img1)
        faces2 = self._detect_face(img2)
        
        if faces1 is None or len(faces1) == 0 or faces2 is None or len(faces2) == 0:
            return {"face_found": False, "similarity": 0.0, "decision": "NO_FACE_DETECTED"}
            
        if len(faces1) > 1 or len(faces2) > 1:
            return {"face_found": True, "similarity": 0.0, "decision": "MULTIPLE_FACES_DETECTED", "message": "Multiple faces detected in the image(s)."}
            
        face1 = faces1[0]
        face2 = faces2[0]

        # Align
        aligned_face1 = self.recognizer.alignCrop(img1, face1)
        aligned_face2 = self.recognizer.alignCrop(img2, face2)

        # Extract features
        feat1 = self.recognizer.feature(aligned_face1)
        feat2 = self.recognizer.feature(aligned_face2)

        # Compare
        score = self.recognizer.match(feat1, feat2, cv2.FaceRecognizerSF_FR_COSINE)
        
        decision = "MATCH" if score >= 0.363 else "MISMATCH"
        
        return {
            "face_found": True,
            "similarity": float(score),
            "decision": decision
        }

def get_face_service() -> FaceVerificationService:
    return FaceVerificationService.get_instance()
