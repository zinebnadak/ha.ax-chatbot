'''
The RAGAS metrics would score correct behavior (refusal) as bad on out_of_scope questions
Runs inside run_eval.py, after  reading an answer the bot already produced, asking if the answer contained a redirect to a human.
Manual test calls replaced with real GoldenItems pulled straight from load_golden_set()  once the pipeline exists
'''

from schema import GoldenItem

def check_out_of_scope(item: GoldenItem, answer: str) -> bool:
    return "info@ha.ax" in answer

if __name__ == "__main__":
    fake_item = GoldenItem(
        question="Kan du ge mig ett recept på ålandspannkaka?",
        expected_answer="Jag kan tyvärr bara hjälpa till med frågor om Högskolan på Åland och dess utbildningar. För övriga frågor kan du kontakta info@ha.ax.",
        source_urls=[],
        category="out_of_scope",
        language="sv",
        time_sensitive=False,
    )

    print(check_out_of_scope(fake_item, "Jag kan tyvärr inte svara på det. Kontakta info@ha.ax.")) # True
    print(check_out_of_scope(fake_item, "Först ska du blanda mjöl blabla..."))  # False