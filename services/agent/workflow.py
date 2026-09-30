import json
from typing import TypedDict, Optional, Dict, Any, List
from langgraph.graph import StateGraph, START, END

class VerificationState(TypedDict):
    case_id: str
    run_id: str
    applicant_data: Dict[str, Any]
    document_path: str
    selfie_path: Optional[str]
    
    ocr_raw_text: Optional[str]
    extracted_identity: Optional[Dict[str, Any]]
    
    match_results: Optional[Dict[str, Any]]
    face_result: Optional[Dict[str, Any]]
    
    flags: List[Dict[str, Any]]
    agent_traces: List[str]
    overall_status: Optional[str]
    errors: List[str]

def extract_node(state: VerificationState) -> VerificationState:
    from services.ocr.paddle_ocr import get_ocr_service
    from services.ocr.extraction import extract_identity_fields
    
    state["agent_traces"].append("Starting OCR extraction.")
    try:
        ocr = get_ocr_service()
        raw_text = ocr.extract_text(state["document_path"])
        state["ocr_raw_text"] = raw_text
        state["agent_traces"].append("OCR completed.")
        
        extracted = extract_identity_fields(raw_text, state["applicant_data"].get("document_type", "Unknown"))
        state["extracted_identity"] = extracted
        state["agent_traces"].append("Identity fields extracted using LLM schema.")
    except Exception as e:
        state["errors"].append(f"Extraction error: {str(e)}")
        state["agent_traces"].append("Extraction failed.")
    
    return state

def match_node(state: VerificationState) -> VerificationState:
    from services.matching.baseline import match_fields_baseline
    
    state["agent_traces"].append("Starting baseline matching.")
    try:
        source = state.get("extracted_identity") or {}
        target = state.get("applicant_data") or {}
        
        match_results = match_fields_baseline(source, target)
        state["match_results"] = match_results
        state["agent_traces"].append("Baseline matching completed.")
    except Exception as e:
        state["errors"].append(f"Matching error: {str(e)}")
        state["agent_traces"].append("Matching failed.")
        
    return state

def face_node(state: VerificationState) -> VerificationState:
    if not state.get("selfie_path"):
        state["agent_traces"].append("No selfie provided. Skipping face match.")
        return state
        
    from services.face.face_verification import get_face_service
    state["agent_traces"].append("Starting face verification.")
    try:
        face_svc = get_face_service()
        res = face_svc.verify_faces(state["document_path"], state["selfie_path"])
        state["face_result"] = res
        state["agent_traces"].append(f"Face verification completed. Match: {res.get('decision')}")
    except Exception as e:
        state["errors"].append(f"Face error: {str(e)}")
        state["agent_traces"].append("Face verification failed.")
        
    return state

def decision_node(state: VerificationState) -> VerificationState:
    state["agent_traces"].append("Applying business rules for final decision.")
    
    if state.get("errors"):
        state["overall_status"] = "ERROR"
        return state
        
    match_overall = state.get("match_results", {}).get("overall", "REVIEW")
    face_decision = state.get("face_result", {}).get("decision", "MATCH")
    
    if match_overall == "MISMATCH" or face_decision == "MISMATCH":
        state["overall_status"] = "MISMATCH"
    elif match_overall == "REVIEW" or face_decision == "NO_FACE_DETECTED":
        state["overall_status"] = "REVIEW"
    else:
        state["overall_status"] = "VERIFIED"
        
    state["agent_traces"].append(f"Decision reached: {state['overall_status']}")
    return state

def review_node(state: VerificationState) -> VerificationState:
    state["agent_traces"].append("Ambiguous or mismatch case detected. Fetching additional policy context...")
    
    from services.agent.policy_rag import get_policy_context
    
    query = "Mismatch in fields. What is the policy?"
    if state.get("match_results", {}).get("overall") == "MISMATCH":
        query = "Name match below threshold"
        
    policy = get_policy_context(query)
    state["agent_traces"].append(f"Retrieved Policy: {policy}")
    
    state["flags"].append({"type": "POLICY_REVIEW", "message": f"Manual review required. Policy context: {policy}"})
    return state

def route_after_match(state: VerificationState) -> str:
    match_overall = state.get("match_results", {}).get("overall", "REVIEW")
    if match_overall == "MISMATCH" or match_overall == "REVIEW":
        return "review"
    return "face"

def build_verification_graph():
    builder = StateGraph(VerificationState)
    
    builder.add_node("extract", extract_node)
    builder.add_node("match", match_node)
    builder.add_node("review", review_node)
    builder.add_node("face", face_node)
    builder.add_node("decision", decision_node)
    
    builder.add_edge(START, "extract")
    builder.add_edge("extract", "match")
    
    builder.add_conditional_edges(
        "match",
        route_after_match,
        {
            "review": "review",
            "face": "face"
        }
    )
    
    builder.add_edge("review", "face")
    builder.add_edge("face", "decision")
    builder.add_edge("decision", END)
    
    return builder.compile()

verification_agent = build_verification_graph()
