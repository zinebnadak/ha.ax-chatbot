'''
Main public faceing protection
For abuse OpenAI's Moderation API that detects harmful content in text and images
For prompt injection regex with word boundaries & text normalization
'''

import re

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
