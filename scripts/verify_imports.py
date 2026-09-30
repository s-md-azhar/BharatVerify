import sys

def check_imports():
    modules = [
        "torch",
        "paddleocr",
        "cv2",
        "google.genai",
        "fastapi",
        "langgraph",
        "sentence_transformers",
        "sqlalchemy",
        "pydantic",
        "uvicorn"
    ]
    
    failed = []
    for mod in modules:
        try:
            __import__(mod)
            print(f"OK: {mod} imported successfully")
        except ImportError as e:
            print(f"ERR: Failed to import {mod}: {e}")
            failed.append(mod)
            
    if failed:
        print("\nSome modules failed to import.")
        sys.exit(1)
    else:
        print("\nAll required modules imported successfully!")

if __name__ == "__main__":
    check_imports()
