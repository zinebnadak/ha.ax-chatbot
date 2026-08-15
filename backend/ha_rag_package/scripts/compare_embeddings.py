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
# Run command: uv run backend/ha_rag_package/scripts/compare_embeddings.py

from pathlib import Path 
import json
from ha_rag_package.app.rag.chunking import chunk_all_pages, load_pages

def load_golden_set(file_path: Path) -> list[dict]:
    with file_path.open("r", encoding="utf-8") as file:
        golden_set_file = json.load(file)

        return [
            item for item in golden_set_file
            if item.get("source_urls")
        ]

def chunk_corpus(pages: list[dict]) -> list[dict]:
    parents, children = chunk_all_pages(pages)

    lookup_dict = {} # tool to attach urls
    for item in parents:
        lookup_dict[item["id"]] = item["url"] # adds/updates one key

    # modifying each child dict by adding a "url" key into it
    for item in children:
        item["url"] = lookup_dict[item["parent_id"]]

    return children



'''
if __name__ == "__main__":

    # Load the golden set
    golden_set_path = Path(__file__).parent.parent / "eval" / "golden_set.json"
    print(load_golden_set(golden_set_path))
'''

    # Chunk corpus
data_folder = Path("data")
pages = load_pages(data_folder)
print(chunk_corpus(pages))



