import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.agent.workflow import build_verification_graph
from langgraph.graph import StateGraph

def test_paths():
    graph = build_verification_graph()
    
    print("Testing Path A: MATCH")
    state_a = {
        "case_id": "test_1",
        "run_id": "run_1",
        "applicant_data": {"document_type": "AADHAAR"},
        "document_path": "dummy.jpg",
        "selfie_path": None,
        "ocr_raw_text": None,
        "extracted_identity": {"name": "Alice"},
        "match_results": {"overall": "MATCH"},
        "face_result": None,
        "flags": [],
        "agent_traces": [],
        "overall_status": None,
        "errors": []
    }
    
    # We can invoke node by node to see routing, but let's just trace it
    # We will just run the graph, but since extract_node and face_node try to do real work (OCR/Face), 
    # we can't easily run it fully without mocking. Let's mock them.
    from unittest.mock import patch
    with patch('services.agent.workflow.extract_node', return_value=state_a), \
         patch('services.agent.workflow.match_node', return_value=state_a), \
         patch('services.agent.workflow.face_node', return_value=state_a):
         
        path_a = ["__start__"]
        for event in graph.stream(state_a):
            for node_name in event.keys():
                path_a.append(node_name)
        print("Path A Node Sequence:", " -> ".join(path_a))
        
    print("\nTesting Path B: MISMATCH")
    state_b = state_a.copy()
    state_b["match_results"] = {"overall": "MISMATCH"}
    state_b["agent_traces"] = []
    
    with patch('services.agent.workflow.extract_node', return_value=state_b), \
         patch('services.agent.workflow.match_node', return_value=state_b), \
         patch('services.agent.workflow.face_node', return_value=state_b):
         
        path_b = ["__start__"]
        for event in graph.stream(state_b):
            for node_name in event.keys():
                path_b.append(node_name)
        print("Path B Node Sequence:", " -> ".join(path_b))
        # It should show review node in Path B

if __name__ == "__main__":
    test_paths()
