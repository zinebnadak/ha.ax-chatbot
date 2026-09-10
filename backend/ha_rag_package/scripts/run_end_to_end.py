'''
This script sends every question from the golden set through the full live chatbot pipeline (retrieval + generation + filters) 
and checks whether out-of-scope questions get refused and in-scope answers cite the right source.
'''

import time
from pathlib import Path
from app.rag.schema import load_golden_set
from app.rag.pipeline import generate_answer

PROJECT_ROOT = Path(__file__).resolve().parents[1]
GOLDEN_PATH = PROJECT_ROOT / "eval" / "golden_set.json"


def check_refusal(answer: str) -> bool:
    """Heuristic: did the bot correctly decline an out-of-scope question?"""
    refusal_markers = ["info@ha.ax", "tyvärr", "can only help", "kan tyvärr bara"]
    return any(marker.lower() in answer.lower() for marker in refusal_markers)


def check_citation(answer: str, source_urls: list[str]) -> bool:
    """Did the bot cite at least one of the expected source URLs?"""
    if not source_urls:
        return True  # nothing to check against
    return any(url.rstrip("/") in answer for url in source_urls)


def run_end_to_end(golden_path=GOLDEN_PATH, sleep_between=0.5):
    items = load_golden_set(golden_path)

    results = []
    for i, item in enumerate(items, start=1):
        print(f"[{i}/{len(items)}] {item.question[:60]}...")

        try:
            answer = generate_answer(query=item.question, language=item.language)
        except Exception as e:
            answer = f"ERROR: {e}"

        if item.category == "out_of_scope":
            passed = check_refusal(answer)
        else:
            passed = check_citation(answer, item.source_urls)

        results.append({
            "question": item.question,
            "category": item.category,
            "language": item.language,
            "answer": answer,
            "passed": passed,
        })

        time.sleep(sleep_between)  # be gentle on rate limits / API

    total = len(results)
    passed_count = sum(r["passed"] for r in results)
    print(f"\n{passed_count}/{total} passed ({round(100 * passed_count / total, 1)}%)\n")

    failures = [r for r in results if not r["passed"]]
    if failures:
        print("--- FAILURES ---")
        for f in failures:
            print(f"\n[{f['category']} / {f['language']}] {f['question']}")
            print(f"  answer: {f['answer'][:200]}")

    return results


if __name__ == "__main__":
    run_end_to_end()