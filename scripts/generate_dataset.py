import json
import random
import uuid
import os
from datetime import datetime, timedelta

NUM_IDENTITIES = 3000

FIRST_NAMES_EN = ["Rahul", "Priya", "Amit", "Sneha", "Vikram", "Anjali", "Rohan", "Pooja", "Karan", "Neha", "Arjun", "Kavita", "Suresh", "Sunita", "Ramesh", "Deepak", "Akash", "Ravi", "Sanjay", "Vinod"]
LAST_NAMES_EN = ["Sharma", "Patel", "Singh", "Kumar", "Gupta", "Deshmukh", "Joshi", "Kulkarni", "Chauhan", "Yadav", "Verma", "Tiwari", "Das", "Rao", "Reddy"]

# For Transliteration tests
HI_TO_EN_NAMES = {
    "राहुल": "Rahul", "प्रिया": "Priya", "अमित": "Amit", "स्नेहा": "Sneha",
    "विक्रम": "Vikram", "अंजलि": "Anjali", "रोहन": "Rohan", "पूजा": "Pooja",
    "शर्मा": "Sharma", "पटेल": "Patel", "सिंह": "Singh", "कुमार": "Kumar"
}
MR_TO_EN_NAMES = {
    "अंजली": "Anjali", "करण": "Karan", "पाटील": "Patil", "सिंग": "Singh",
    "देशमुख": "Deshmukh", "कुलकर्णी": "Kulkarni"
}

FIRST_NAMES_HI = ["राहुल", "प्रिया", "अमित", "स्नेहा", "विक्रम", "अंजलि", "रोहन", "पूजा", "करन", "नेहा"]
LAST_NAMES_HI = ["शर्मा", "पटेल", "सिंह", "कुमार", "गुप्ता", "देशमुख", "जोशी", "कुलकर्णी", "चौहान", "यादव"]
FIRST_NAMES_MR = ["राहुल", "प्रिया", "अमित", "स्नेहा", "विक्रम", "अंजली", "रोहन", "पूजा", "करण", "नेहा"]
LAST_NAMES_MR = ["शर्मा", "पाटील", "सिंग", "कुमार", "गुप्ता", "देशमुख", "जोशी", "कुलकर्णी", "चौहान", "यादव"]

CITIES_EN = ["Mumbai", "Pune", "Delhi", "Nagpur", "Nashik", "Thane", "Aurangabad", "Solapur", "Kolhapur", "Amravati"]
CITIES_HI = ["मुंबई", "पुणे", "दिल्ली", "नागपुर", "नाशिक", "ठाणे", "औरंगाबाद", "सोलापुर", "कोल्हापुर", "अमरावती"]
CITIES_MR = ["मुंबई", "पुणे", "दिल्ली", "नागपूर", "नाशिक", "ठाणे", "छत्रपती संभाजीनगर", "सोलापूर", "कोल्हापूर", "अमरावती"]
STATES_EN = ["Maharashtra", "Delhi", "Gujarat", "Karnataka", "Uttar Pradesh"]
STATES_HI = ["महाराष्ट्र", "दिल्ली", "गुजरात", "कर्नाटक", "उत्तर प्रदेश"]
STATES_MR = ["महाराष्ट्र", "दिल्ली", "गुजरात", "कर्नाटक", "उत्तर प्रदेश"]

def random_date(start_year=1950, end_year=2005):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    return (start_date + timedelta(days=random_days)).strftime("%d/%m/%Y")

def random_pin():
    return str(random.randint(400000, 499999))

def random_doc_id():
    return f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(1000000, 9999999)}"

def generate_identity(lang="EN"):
    if lang == "EN":
        fn, ln = random.choice(FIRST_NAMES_EN), random.choice(LAST_NAMES_EN)
        ffn, fln = random.choice(FIRST_NAMES_EN), ln
        city, state = random.choice(CITIES_EN), random.choice(STATES_EN)
        address = f"{random.randint(1, 100)}, Main Road, {city}, {state}"
    elif lang == "HI":
        fn, ln = random.choice(FIRST_NAMES_HI), random.choice(LAST_NAMES_HI)
        ffn, fln = random.choice(FIRST_NAMES_HI), ln
        city, state = random.choice(CITIES_HI), random.choice(STATES_HI)
        address = f"{random.randint(1, 100)}, मुख्य मार्ग, {city}, {state}"
    else: # MR
        fn, ln = random.choice(FIRST_NAMES_MR), random.choice(LAST_NAMES_MR)
        ffn, fln = random.choice(FIRST_NAMES_MR), ln
        city, state = random.choice(CITIES_MR), random.choice(STATES_MR)
        address = f"{random.randint(1, 100)}, मुख्य रस्ता, {city}, {state}"

    return {
        "identity_id": str(uuid.uuid4()),
        "lang": lang,
        "name": f"{fn} {ln}",
        "father_name": f"{ffn} {fln}",
        "dob": random_date(),
        "gender": random.choice(["Male", "Female", "M", "F"]),
        "address": address,
        "state": state,
        "city": city,
        "district": city,
        "pin": random_pin(),
        "document_id": random_doc_id()
    }

def generate_positive_pair(identity):
    copy_id = identity.copy()
    variations = []
    
    variation_type = random.choice(["exact", "ocr_typo", "translit", "spelling_variant", "token_reorder", "punct_diff", "whitespace_diff", "difficult_addr"])
    
    if variation_type == "ocr_typo":
        if len(copy_id["name"]) > 5:
            idx = random.randint(1, len(copy_id["name"]) - 2)
            name_list = list(copy_id["name"])
            name_list[idx] = random.choice(['1', 'l', '0', 'O', 'I']) # Common OCR errors
            copy_id["name"] = "".join(name_list)
            variations.append("ocr_typo")
    
    elif variation_type == "translit":
        # Simulate cross-language transliteration (e.g. Hindi document, English application)
        name_parts = copy_id["name"].split(" ")
        new_parts = []
        for p in name_parts:
            new_parts.append(HI_TO_EN_NAMES.get(p, MR_TO_EN_NAMES.get(p, p)))
        if new_parts != name_parts:
            copy_id["name"] = " ".join(new_parts)
            variations.append("transliteration")

    elif variation_type == "spelling_variant":
        # Simulating spelling variants like Pooja -> Puja
        variants = {"Pooja": "Puja", "Rahul": "Rahool", "Sneha": "Snehaa", "Karan": "Karann", "Chauhan": "Chouhan"}
        for k, v in variants.items():
            if k in copy_id["name"]:
                copy_id["name"] = copy_id["name"].replace(k, v)
                variations.append("spelling_variant")
                break

    elif variation_type == "token_reorder":
        parts = copy_id["name"].split(" ")
        if len(parts) > 1:
            parts.reverse()
            copy_id["name"] = " ".join(parts)
            variations.append("token_reorder")

    elif variation_type == "punct_diff":
        copy_id["address"] = copy_id["address"].replace(",", "").replace(".", "")
        copy_id["name"] = copy_id["name"] + "."
        variations.append("punct_diff")

    elif variation_type == "whitespace_diff":
        copy_id["father_name"] = copy_id["father_name"].replace(" ", "  ")
        copy_id["name"] = " " + copy_id["name"] + " "
        variations.append("whitespace_diff")

    elif variation_type == "difficult_addr":
        if "Main Road" in copy_id["address"]:
            copy_id["address"] = copy_id["address"].replace("Main Road", "M.R.")
            variations.append("address_abbr")
        elif "मुख्य मार्ग" in copy_id["address"]:
            copy_id["address"] = copy_id["address"].replace("मुख्य मार्ग", "मु.मा.")
            variations.append("address_abbr")

    return {
        "source": identity,
        "application": copy_id,
        "label": 1,
        "variations": variations if variations else ["exact"]
    }

def generate_negative_pair(id1, id2):
    copy_id = id1.copy()
    variations = []
    
    variation_type = random.choice(["similar_name", "same_surname", "same_address", "wrong_dob", "wrong_pin", "mixed_fields", "completely_different"])
    
    if variation_type == "similar_name":
        # Same surname, completely different first name
        fn, ln = copy_id["name"].split(" ")[0], copy_id["name"].split(" ")[-1]
        copy_id["name"] = f"Rajat {ln}" # Hardcode a different name
        variations.append("similar_name")
        
    elif variation_type == "same_surname":
        fn, ln = copy_id["name"].split(" ")[0], copy_id["name"].split(" ")[-1]
        fn2, ln2 = id2["name"].split(" ")[0], id2["name"].split(" ")[-1]
        copy_id["name"] = f"{fn2} {ln}"
        variations.append("same_surname_different_person")
        
    elif variation_type == "same_address":
        copy_id = id2.copy()
        copy_id["address"] = id1["address"]
        variations.append("same_address_different_person")
        
    elif variation_type == "wrong_dob":
        # Same everything, different DOB
        copy_id["dob"] = id2["dob"]
        variations.append("wrong_dob")
        
    elif variation_type == "wrong_pin":
        copy_id["pin"] = id2["pin"]
        variations.append("wrong_pin")
        
    elif variation_type == "mixed_fields":
        copy_id["name"] = id1["name"]
        copy_id["father_name"] = id2["father_name"]
        copy_id["address"] = id2["address"]
        copy_id["dob"] = id1["dob"]
        variations.append("mixed_fields")
        
    else:
        copy_id = id2.copy()
        variations.append("completely_different")

    return {
        "source": id1,
        "application": copy_id,
        "label": 0,
        "variations": variations
    }

def main():
    print(f"Generating {NUM_IDENTITIES} identities...")
    identities = []
    for _ in range(NUM_IDENTITIES):
        lang = random.choice(["EN", "HI", "MR"])
        identities.append(generate_identity(lang))
        
    # Disjoint splits: test identities are never seen in training
    random.shuffle(identities)
    
    train_split = int(0.7 * NUM_IDENTITIES)
    val_split = int(0.85 * NUM_IDENTITIES)
    
    train_identities = identities[:train_split]
    val_identities = identities[train_split:val_split]
    test_identities = identities[val_split:]
    
    print(f"Split: {len(train_identities)} train, {len(val_identities)} val, {len(test_identities)} test.")
    
    def generate_pairs_for_split(split_identities):
        pairs = []
        # For each identity, generate 1 positive pair and 1 negative pair
        for i, ident in enumerate(split_identities):
            pairs.append(generate_positive_pair(ident))
            
            # Pick a random other identity for negative pair within the SAME SPLIT
            other_idx = random.randint(0, len(split_identities) - 1)
            while other_idx == i and len(split_identities) > 1:
                other_idx = random.randint(0, len(split_identities) - 1)
                
            pairs.append(generate_negative_pair(ident, split_identities[other_idx]))
        return pairs

    train_pairs = generate_pairs_for_split(train_identities)
    val_pairs = generate_pairs_for_split(val_identities)
    test_pairs = generate_pairs_for_split(test_identities)
    
    os.makedirs("datasets/synthetic", exist_ok=True)
    
    with open("datasets/synthetic/identities.json", "w", encoding="utf-8") as f:
        json.dump(identities, f, ensure_ascii=False, indent=2)
        
    with open("datasets/synthetic/train_pairs.json", "w", encoding="utf-8") as f:
        json.dump(train_pairs, f, ensure_ascii=False, indent=2)
        
    with open("datasets/synthetic/val_pairs.json", "w", encoding="utf-8") as f:
        json.dump(val_pairs, f, ensure_ascii=False, indent=2)
        
    with open("datasets/synthetic/test_pairs.json", "w", encoding="utf-8") as f:
        json.dump(test_pairs, f, ensure_ascii=False, indent=2)
        
    print("Dataset generation complete. Files saved to datasets/synthetic/")

if __name__ == "__main__":
    main()
