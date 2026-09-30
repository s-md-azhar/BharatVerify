import os
import sys
import Levenshtein
import cv2
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.ocr.paddle_ocr import get_ocr_service
from scripts.test_ocr_faces import create_synthetic_doc

def evaluate_ocr():
    ocr = get_ocr_service()
    
    test_cases = [
        {"lang": "English", "text": "Name: Rahul Sharma\nDOB: 15/08/1990\nAddress: 42, Main Road, Mumbai"},
        {"lang": "Hindi", "text": "नाम: राहुल शर्मा\nजन्म तिथि: 15/08/1990\nपता: 42, मुख्य मार्ग, मुंबई"},
        {"lang": "Marathi", "text": "नाव: राहुल शर्मा\nजन्म तारीख: 15/08/1990\nपत्ता: 42, मुख्य रस्ता, मुंबई"}
    ]
    
    os.makedirs("datasets/test_ocr", exist_ok=True)
    
    print("--- OCR METRICS ---")
    print(f"Total documents tested: {len(test_cases)}")
    
    for case in test_cases:
        path = f"datasets/test_ocr/{case['lang']}.jpg"
        create_synthetic_doc(case['text'], path)
        
        # Make it challenging using OpenCV
        img = cv2.imread(path)
        img = cv2.GaussianBlur(img, (3, 3), 0)
        noise = np.random.normal(0, 5, img.shape).astype(np.uint8)
        img = cv2.add(img, noise)
        cv2.imwrite(path, img)
        
        extracted = ocr.extract_text(path).strip()
        
        # Calculate Character Error Rate (CER)
        dist = Levenshtein.distance(case['text'], extracted)
        cer = dist / max(len(case['text']), 1)
        
        # Calculate Word Error Rate (WER)
        orig_words = case['text'].split()
        ext_words = extracted.split()
        
        # Simple word match ratio
        matched_words = sum(1 for w in orig_words if w in ext_words)
        wer = 1.0 - (matched_words / max(len(orig_words), 1))
        
        print(f"\nLanguage: {case['lang']}")
        print(f"Original Length: {len(case['text'])} chars, Extracted: {len(extracted)} chars")
        print(f"CER: {cer:.4f}")
        print(f"WER (approx): {wer:.4f}")
        
if __name__ == "__main__":
    evaluate_ocr()
