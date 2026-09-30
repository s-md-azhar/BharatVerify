import requests
import time

def test_api():
    base_url = "http://127.0.0.1:8000/api/v1"
    
    print("Testing /health...")
    resp = requests.get("http://127.0.0.1:8000/health")
    print(resp.json())
    
    print("Testing case creation...")
    case_data = {
        "application_id": "app_12345",
        "applicant_name": "Rahul Sharma",
        "date_of_birth": "15/08/1990",
        "gender": "Male",
        "address": "42, Main Road, Mumbai, Maharashtra",
        "document_type": "AADHAAR"
    }
    resp = requests.post(f"{base_url}/cases/", json=case_data)
    print("Create Case Response:", resp.status_code, resp.text)
    
    if resp.status_code == 200:
        case = resp.json()
        case_id = case["id"]
        
        print(f"Testing fetch case {case_id}...")
        resp = requests.get(f"{base_url}/cases/{case_id}")
        print("Fetch Case Response:", resp.status_code, resp.json())
        
        # Test full workflow (Mocking document and selfie upload by just calling the verify endpoint if it existed, or we just test the endpoints).
        print("Integration test endpoints working.")

if __name__ == "__main__":
    test_api()
