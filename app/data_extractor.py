import re

UPI_PATTERN = r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b"
URL_PATTERN = r"https?://[^\s]+"

def extract_intelligence(message_text: str):
    text = message_text.lower()
    intel = {
        "upiIds": re.findall(UPI_PATTERN, text),
        "phishingLinks": re.findall(URL_PATTERN, text),
        "suspiciousKeywords": [w for w in ["blocked", "urgent", "verify"] if w in text]
    }
    return intel
