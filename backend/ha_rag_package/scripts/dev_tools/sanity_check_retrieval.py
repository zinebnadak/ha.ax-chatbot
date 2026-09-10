from pathlib import Path
from app.rag.schema import load_golden_set
from app.rag.retrieval import retrieve_with_context

PROJECT_ROOT = Path(__file__).resolve().parents[1]  # scripts/ -> ha_rag_package/
DEFAULT_GOLDEN_PATH = PROJECT_ROOT / "eval" / "golden_set.json"



def normalize_url(url: str) -> str:
    return url.rstrip("/").lower()

def run_sanity_check(golden_path=DEFAULT_GOLDEN_PATH, k=5):
    items = load_golden_set(golden_path)
    testable = [i for i in items if i.category != "out_of_scope"]

    hits, misses, miss_log = 0, 0, []

    for item in testable:
        expected = {normalize_url(u) for u in item.source_urls}
        if not expected:
            continue

        results = retrieve_with_context(item.question, k=k)
        retrieved_urls = {normalize_url(r["url"]) for r in results}

        if expected & retrieved_urls:
            hits += 1
        else:
            misses += 1
            miss_log.append({
                "question": item.question,
                "category": item.category,
                "language": item.language,
                "expected": list(expected),
                "got": [r["url"] for r in results],
            })

    total = hits + misses
    print(f"\n{hits}/{total} hit expected source in top-{k} ({round(100*hits/total, 1)}%)\n")

    if miss_log:
        print("--- MISSES ---")
        for m in miss_log:
            print(f"\n[{m['category']} / {m['language']}] {m['question']}")
            print(f"expected: {m['expected']}")
            print(f"got:      {m['got']}")

    return hits, misses, miss_log

if __name__ == "__main__":
    run_sanity_check()