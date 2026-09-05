'''
Main public faceing protection
For abuse OpenAI's Moderation API that detects harmful content in text and images
For prompt injection regex with word boundaries & text normalization
'''

import re

MAX_LENGTH = 1000

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions",
    r"disregard\s+(all\s+)?(previous|prior|above)\s+instructions",
    r"you\s+are\s+now\s+(a|an)\b",
    r"reveal\s+(your\s+)?(system\s+)?prompt",
    r"(show|print|repeat)\s+(your\s+)?(system\s+)?prompt",
    r"act\s+as\s+(a|an)\b",
    r"pretend\s+(you\s+are|to\s+be)\b",
    r"jailbreak",
    r"developer\s+mode",
]

_compiled_patterns = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]

def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def _check_injection(message: str) -> bool:
    normalized = _normalize(message)
    return any(pattern.search(normalized) for pattern in _compiled_patterns)

def filter_input(message: str, language: str = "English") -> tuple[bool, str]:
    is_swedish = language.strip().lower().startswith("sv")

    if not message or not message.strip():
        return False, "Vänligen skriv en fråga." if is_swedish else "Please enter a question."

    if len(message) > MAX_LENGTH:
        if is_swedish:
            return False, f"Ditt meddelande är för långt (max {MAX_LENGTH} tecken)."
        return False, f"Your message is too long (max {MAX_LENGTH} characters)."

    if _check_injection(message):
        if is_swedish:
            return False, "Jag kan inte behandla den förfrågan. Ställ en fråga om Högskolan på Åland."
        return False, "I can't process that request. Please ask a question about Högskolan på Åland."

    return True, message.strip()