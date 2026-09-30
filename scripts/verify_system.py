import os
import sys
import time
import requests
import psycopg2

def verify():
    print("--- 1. Checking .env ---")
    if not os.path.exists(".env"):
        print("FAIL: .env does not exist.")
    else:
        with open(".env", "r") as f:
            content = f.read()
        if "GEMINI_API_KEY=" in content:
            print("PASS: GEMINI_API_KEY is configured.")
        else:
            print("FAIL: GEMINI_API_KEY missing.")
            
    print("\n--- 2. Checking .gitignore ---")
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            if ".env" in f.read():
                print("PASS: .env is ignored.")
            else:
                print("FAIL: .env not in .gitignore.")
    else:
        print("FAIL: .gitignore missing.")
        
    print("\n--- 3. Checking Dependencies ---")
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import psycopg2
        import sentence_transformers
        import pydantic
        import faiss
        import PIL
        from google import genai
        print("PASS: All major dependencies imported.")
    except ImportError as e:
        print(f"FAIL: Dependency import failed: {e}")
        
    print("\n--- 4/5. Checking PostgreSQL ---")
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # Load from .env manually if not in env
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("DATABASE_URL="):
                    db_url = line.strip().split("=")[1]
                    break
    
    if db_url:
        try:
            conn = psycopg2.connect(db_url)
            print("PASS: PostgreSQL connection successful.")
            conn.close()
        except Exception as e:
            print(f"FAIL: Could not connect to Postgres: {e}")
    else:
        print("FAIL: DATABASE_URL not set.")
        
    print("\n--- 6. Backend API Check ---")
    try:
        r = requests.get("http://127.0.0.1:8000/health")
        if r.status_code == 200:
            print("PASS: /health endpoint is alive.")
        else:
            print(f"FAIL: /health returned {r.status_code}")
    except Exception as e:
        print("FAIL: FastAPI server is not running on 8000. Start it to verify.")

if __name__ == "__main__":
    verify()
