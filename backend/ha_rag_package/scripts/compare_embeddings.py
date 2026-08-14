'''
Compare embeddings retrival quality against any golden set (obs the dicts needs to have the same shape to use urls as ground_truth). Metrics: Recall@k and MRR (Mean Reciprocal Rank)

Flow: 
1. pre-embed the corpus once per model (cache to disk so repeat runs are free)
2. loop on terminal input for a question index
3. print all models answers and compare retrieval quality, or compare each models top-k (k *number of chunks most similar to the query) OR just use a similarity threshold

Models I will be comparing:
- `text-embedding-3-small`
- `text-embedding-3-large
- google gemini embeddings 001
- cohere embed v4 
- voyage multilingual -2`

'''


from pathlib import Path 
import json

def load_golden_set(file_path: Path) -> list[dict]:
    with file_path.open("r", encoding="utf-8") as file:
        golden_set_file = json.load(file)

        return [
            item for item in golden_set_file
            if item.get("source_urls")
        ] 

if __name__ == "__main__":
    golden_set_path = Path(__file__).parent.parent / "eval" / "golden_set.json"
    print(load_golden_set(golden_set_path))


def embed_texts (model_name: str, texts: list[str]) -> list[list[float]]
