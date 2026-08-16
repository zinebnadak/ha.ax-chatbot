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
from typing import Callable
import numpy as np

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

# should do ONE job
def embed_chunks (children: list[dict], embedding_fn: Callable[[str], list[float]] ) -> list[dict]: 
    for item in children:
        item["embedding"] = embedding_fn(item["text"]) # fn returns list[float] eg. the embedding 
    
    return children

# should do ONE job
def embed_question(question: str, embedding_fn: Callable[[str], list[float]] ) -> list[float]:
    return embedding_fn(question)

# function computing cosine similarity
def cosine_similarity(child_embedding: list[float], question_embedding: list[float]) -> float:
    dot_product = np.dot_product(vec_a, vec_b)
    magnitude_a = np.linalg.norm(vec_a)
    magnitude_b = np.linalg.norm(vec_b)
    return dot_product / (magnitude_a * magnitude_b) 

def retrieve_top_k(children: list[dict], question_embedding: list[float], k: int) -> list[dict]:
    child_similarity_scores = [] # a list of tuples with score and full child dict
    for item in children:
        compute_cos_sim = cosine_similarity(item["embedding"], question_embedding)
        child_similarity_scores.append((compute_cos_sim, item))

    sorted_similarity_scores = sorted(child_similarity_scores, key=lambda x: x[0], reverse=True) # sort by score only. The whole tuple will throw an error comparing dicts...
    top_k_items = [tuple_item[1] for tuple_item in sorted_similarity_scores[:k]] # top k, item in the tuple
    return top_k_items

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



