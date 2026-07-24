# eval-set item validation

from pydantic import BaseModel
from typing import Literal
from pathlib import Path
import json

THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parent.parent  # evals/schema.py -> project root
GOLDEN_SET_PATH = PROJECT_ROOT / "data" / "golden_set" / "golden_set.json"


class GoldenItem(BaseModel):
    question: str
    expected_answer: str
    source_urls: list[str]
    category: Literal[
        "programme_coverage", "wrong_programme_facts", "wrong_procedure",
        "scope_creep", "dead_end_answer", "out_of_scope", "cross_language_retrieval"
    ]
    language: Literal["sv", "en"]
    time_sensitive: bool


def load_golden_set(path: str | Path) -> list[GoldenItem]:
    with open(path, "r", encoding="utf-8") as file:
        golden_set = json.load(file)

    return [GoldenItem(**entry) for entry in golden_set]


if __name__ == "__main__":
    items = load_golden_set(GOLDEN_SET_PATH)
    print(f"Loaded {len(items)} items successfully")