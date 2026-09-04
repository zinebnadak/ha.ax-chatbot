# schema.py
import json
from dataclasses import dataclass

@dataclass
class GoldenItem:
    question: str
    expected_answer: str
    source_urls: list[str]
    category: str
    language: str
    time_sensitive: bool

def load_golden_set(path: str) -> list[GoldenItem]:
    with open(path, "r", encoding="utf-8") as f:
        raw_items = json.load(f)

    return [
        GoldenItem(
            question=item["question"],
            expected_answer=item["expected_answer"],
            source_urls=item["source_urls"],
            category=item["category"],
            language=item["language"],
            time_sensitive=item["time_sensitive"],
        )
        for item in raw_items
    ]