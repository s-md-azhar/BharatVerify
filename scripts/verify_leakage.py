import json

def verify_leakage():
    splits = ["train", "val", "test"]
    ids_per_split = {}
    
    for split in splits:
        with open(f"datasets/synthetic/{split}_pairs.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Extract unique document numbers (or names) from source as identity indicator
        ids = set()
        for item in data:
            ids.add(item["source"]["name"] + item["source"]["dob"])
        ids_per_split[split] = ids
        
    train_val = ids_per_split["train"].intersection(ids_per_split["val"])
    train_test = ids_per_split["train"].intersection(ids_per_split["test"])
    val_test = ids_per_split["val"].intersection(ids_per_split["test"])
    
    print(f"Train/Val intersection: {len(train_val)}")
    print(f"Train/Test intersection: {len(train_test)}")
    print(f"Val/Test intersection: {len(val_test)}")
    
    if len(train_val) == 0 and len(train_test) == 0 and len(val_test) == 0:
        print("✅ SUCCESS: No identity leakage between splits.")
    else:
        print("❌ ERROR: Identity leakage detected!")

if __name__ == "__main__":
    verify_leakage()
