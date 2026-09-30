import re
import unicodedata

def normalize_text(text: str) -> str:
    """Normalize general text by removing extra whitespace and lowercasing."""
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()
    text = re.sub(r'[\.,;:\-\'\"()\[\]{}]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_address(address: str) -> str:
    """Address specific normalization like expanding abbreviations."""
    if not isinstance(address, str):
        return ""
    address = normalize_text(address)
    
    # Simple abbreviations map
    abbreviations = {
        r'\bm r\b': 'main road',
        r'\bm\.r\.\b': 'main road',
        r'\bmain rd\b': 'main road',
        r'\bsec\b': 'sector',
        r'\bst\b': 'street',
        r'\bdist\b': 'district',
        r'\bpin\b': 'pincode',
    }
    
    for pattern, replacement in abbreviations.items():
        address = re.sub(pattern, replacement, address)
        
    return address

def normalize_date(date_str: str) -> str:
    """Convert various date formats to YYYY-MM-DD for deterministic comparison."""
    if not isinstance(date_str, str):
        return ""
    
    # Typical variants: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD
    parts = re.split(r'[/.-]', date_str.strip())
    if len(parts) == 3:
        # Check if first part is YYYY
        if len(parts[0]) == 4:
            return f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
        elif len(parts[2]) == 4:
            return f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
    return date_str

def normalize_gender(gender_str: str) -> str:
    """Normalize gender to standard categories."""
    if not isinstance(gender_str, str):
        return ""
    gender_str = gender_str.lower().strip()
    if gender_str in ['m', 'male', 'पुरुष']:
        return 'MALE'
    if gender_str in ['f', 'female', 'महिला']:
        return 'FEMALE'
    if gender_str in ['t', 'transgender', 'other', 'अन्य']:
        return 'OTHER'
    return 'UNKNOWN'
