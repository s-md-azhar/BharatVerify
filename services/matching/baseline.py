from typing import Dict, Any
from .normalize import normalize_text, normalize_address, normalize_date, normalize_gender
from .features import compute_all_features

def match_fields_baseline(source: Dict[str, Any], target: Dict[str, Any]) -> Dict[str, Any]:
    """
    Baseline deterministic/fuzzy matching without ML embeddings.
    """
    results = {}
    
    # 1. Name Match
    sn = normalize_text(source.get("name", ""))
    tn = normalize_text(target.get("name", ""))
    name_feats = compute_all_features(sn, tn)
    
    name_score = (name_feats["fuzzy"] * 0.5) + (name_feats["token"] * 0.5)
    name_decision = "MATCH" if name_score > 0.85 else "REVIEW" if name_score > 0.6 else "MISMATCH"
    
    results["name"] = {
        "score": name_score,
        "decision": name_decision,
        "features": name_feats
    }
    
    # 2. DOB Match
    sd = normalize_date(source.get("dob", ""))
    td = normalize_date(target.get("dob", ""))
    dob_score = 1.0 if sd == td and sd != "" else 0.0
    results["dob"] = {
        "score": dob_score,
        "decision": "MATCH" if dob_score == 1.0 else "MISMATCH",
        "features": {"exact": dob_score}
    }
    
    # 3. Address Match
    sa = normalize_address(source.get("address", ""))
    ta = normalize_address(target.get("address", ""))
    addr_feats = compute_all_features(sa, ta)
    
    addr_score = addr_feats["token"]
    addr_decision = "MATCH" if addr_score > 0.7 else "REVIEW" if addr_score > 0.4 else "MISMATCH"
    
    results["address"] = {
        "score": addr_score,
        "decision": addr_decision,
        "features": addr_feats
    }
    
    # 4. Gender Match
    sg = normalize_gender(source.get("gender", ""))
    tg = normalize_gender(target.get("gender", ""))
    gen_score = 1.0 if sg == tg and sg != "UNKNOWN" else 0.0
    results["gender"] = {
        "score": gen_score,
        "decision": "MATCH" if gen_score == 1.0 else "REVIEW"
    }

    # Aggregate decision
    matches = sum(1 for v in results.values() if v["decision"] == "MATCH")
    mismatches = sum(1 for v in results.values() if v["decision"] == "MISMATCH")
    
    overall = "REVIEW"
    if matches >= 3 and mismatches == 0:
        overall = "VERIFIED"
    elif mismatches >= 2:
        overall = "MISMATCH"
        
    return {
        "overall": overall,
        "fields": results
    }
