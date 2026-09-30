import json
import collections

def audit_dataset():
    print("--- FORENSIC AUDIT OF EVALUATION PIPELINE ---")
    
    with open("datasets/synthetic/identities.json", "r", encoding="utf-8") as f:
        identities = json.load(f)
    
    with open("datasets/synthetic/train_pairs.json", "r", encoding="utf-8") as f:
        train_pairs = json.load(f)
        
    with open("datasets/synthetic/val_pairs.json", "r", encoding="utf-8") as f:
        val_pairs = json.load(f)
        
    with open("datasets/synthetic/test_pairs.json", "r", encoding="utf-8") as f:
        test_pairs = json.load(f)
        
    # Get IDs for each split
    train_ids = set([p["source"]["identity_id"] for p in train_pairs] + [p["application"]["identity_id"] for p in train_pairs])
    val_ids = set([p["source"]["identity_id"] for p in val_pairs] + [p["application"]["identity_id"] for p in val_pairs])
    test_ids = set([p["source"]["identity_id"] for p in test_pairs] + [p["application"]["identity_id"] for p in test_pairs])
    
    overlap_train_val = train_ids.intersection(val_ids)
    overlap_train_test = train_ids.intersection(test_ids)
    overlap_val_test = val_ids.intersection(test_ids)
    
    print(f"Total Unique Identities Generated: {len(identities)}")
    print(f"Identities in Train Split: {len(train_ids)}")
    print(f"Identities in Val Split: {len(val_ids)}")
    print(f"Identities in Test Split: {len(test_ids)}")
    
    print(f"\nIdentity Overlap (Train/Val): {len(overlap_train_val)}")
    print(f"Identity Overlap (Train/Test): {len(overlap_train_test)}")
    print(f"Identity Overlap (Val/Test): {len(overlap_val_test)}")
    
    print(f"\nTotal Train Pairs: {len(train_pairs)}")
    print(f"Total Val Pairs: {len(val_pairs)}")
    print(f"Total Test Pairs: {len(test_pairs)}")
    
    def analyze_pairs(name, pairs):
        pos = sum(1 for p in pairs if p["label"] == 1)
        neg = sum(1 for p in pairs if p["label"] == 0)
        
        # Check duplicates
        seen = set()
        dupes = 0
        for p in pairs:
            # Hashable representation of a pair
            pair_hash = f'{p["source"]["identity_id"]}_{p["application"]["identity_id"]}_{p["label"]}'
            if pair_hash in seen:
                dupes += 1
            seen.add(pair_hash)
            
        print(f"{name} -> Positive: {pos}, Negative: {neg}, Duplicates: {dupes}")
        
    analyze_pairs("Train", train_pairs)
    analyze_pairs("Val", val_pairs)
    analyze_pairs("Test", test_pairs)
    
    # Feature dimension check will be run via train_matcher output since it computes embeddings.
    
if __name__ == "__main__":
    audit_dataset()
