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

