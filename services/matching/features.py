import difflib
from typing import Set

def exact_match(s1: str, s2: str) -> float:
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    return 1.0 if s1 == s2 else 0.0

def fuzzy_match(s1: str, s2: str) -> float:
    """Uses difflib SequenceMatcher for similarity ratio (0.0 to 1.0)."""
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    return difflib.SequenceMatcher(None, s1, s2).ratio()

def get_tokens(s: str) -> Set[str]:
    return set(s.split())

def token_overlap(s1: str, s2: str) -> float:
    """Jaccard similarity on tokens."""
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
        
    t1 = get_tokens(s1)
    t2 = get_tokens(s2)
    
    if not t1 and not t2:
        return 1.0
        
    intersection = t1.intersection(t2)
    union = t1.union(t2)
    
    return len(intersection) / len(union) if union else 0.0

def get_char_ngrams(s: str, n: int = 3) -> Set[str]:
    s = f"^{s}$"
    return set(s[i:i+n] for i in range(max(1, len(s) - n + 1)))

def char_ngram_similarity(s1: str, s2: str, n: int = 3) -> float:
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
        
    ng1 = get_char_ngrams(s1, n)
    ng2 = get_char_ngrams(s2, n)
    
    if not ng1 and not ng2:
        return 1.0
        
    intersection = ng1.intersection(ng2)
    union = ng1.union(ng2)
    
    return len(intersection) / len(union) if union else 0.0

def compute_all_features(s1: str, s2: str) -> dict:
    """Compute standard feature dictionary for two strings."""
    return {
        "exact": exact_match(s1, s2),
        "fuzzy": fuzzy_match(s1, s2),
        "token": token_overlap(s1, s2),
        "ngram": char_ngram_similarity(s1, s2)
    }
