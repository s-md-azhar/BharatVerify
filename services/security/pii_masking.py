import re

def mask_aadhar(text: str) -> str:
    """Masks Aadhaar numbers, leaving only last 4 digits."""
    # Matches 12 digit numbers, with optional spaces or hyphens
    pattern = r'\b(\d{4}[\s-]?\d{4}[\s-]?\d{4})\b'
    
    def replacer(match):
        raw = match.group(1)
        clean = re.sub(r'[\s-]', '', raw)
        return f"XXXX-XXXX-{clean[-4:]}"
        
    return re.sub(pattern, replacer, text)

def mask_pan(text: str) -> str:
    """Masks PAN numbers, showing only first 2 and last 2 characters."""
    pattern = r'\b([A-Z]{5}\d{4}[A-Z]{1})\b'
    
    def replacer(match):
        raw = match.group(1)
        return f"{raw[:2]}XXXXXX{raw[-2:]}"
        
    return re.sub(pattern, replacer, text)

def mask_pii_in_logs(log_entry: str) -> str:
    """Masks sensitive PII in log entries before writing to storage/audit."""
    log_entry = mask_aadhar(log_entry)
    log_entry = mask_pan(log_entry)
    return log_entry
