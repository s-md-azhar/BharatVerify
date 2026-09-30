import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.agent.workflow import build_verification_graph
from app.models.domain import VerificationCase

def test_workflow():
    print("Testing LangGraph Agent Workflow...")
    graph = build_verification_graph()
    
    # Just a mock input since we don't have real images uploaded
    state = {
        "case_id": "test_case_123",
        "selfie_path": "dummy_selfie.jpg",
        "document_path": "dummy_doc.jpg",
        "raw_text": "",
        "extracted_data": {},
        "face_match_result": {},
        "db_match_result": {},
        "flags": [],
        "decision": "PENDING"
    }
    
    # We won't actually invoke it fully because we don't have dummy images 
    # and Paddle OCR would fail on them or it will try to call LLMs with dummy text.
    print("Graph built successfully!")
    print("Nodes:", graph.nodes.keys() if hasattr(graph, 'nodes') else "built")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    test_workflow()
