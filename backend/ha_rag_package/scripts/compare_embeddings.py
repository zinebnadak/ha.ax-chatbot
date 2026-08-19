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
- voyage multilingual-2`

'''

# Run command: uv run backend/ha_rag_package/scripts/compare_embeddings.py

'''
EMBEDDING_MODELS = {
    "text-embedding-3-small": embed_with_openai_small,
    "text-embedding-3-large": embed_with_openai_large,
    "google-gemini-embeddings-001": embed_with_gemini_001,
    "cohere-embed-v4": embed_with_cohere_v4,
    "voyage-multilingual-2": embed_with_voyagemultilingual_2
}
'''

from pathlib import Path 
import json
from ha_rag_package.app.rag.chunking import chunk_all_pages, load_pages
from typing import Callable
import numpy as np

from dotenv import load_dotenv
from openai import OpenAI

# load environment variables and create client instances once. 
load_dotenv()
client = OpenAI()

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
    dot = np.dot(child_embedding, question_embedding)
    magnitude_a = np.linalg.norm(child_embedding)
    magnitude_b = np.linalg.norm(question_embedding)
    return dot / (magnitude_a * magnitude_b)

def retrieve_top_k(children: list[dict], question_embedding: list[float], k: int) -> list[dict]:
    child_similarity_scores = [] # a list of tuples with score and full child dict
    for item in children:
        compute_cos_sim = cosine_similarity(item["embedding"], question_embedding)
        child_similarity_scores.append((compute_cos_sim, item))

    sorted_similarity_scores = sorted(child_similarity_scores, key=lambda x: x[0], reverse=True) # sort by score only. The whole tuple will throw an error comparing dicts...
    top_k_items = [tuple_item[1] for tuple_item in sorted_similarity_scores[:k]] # top k, item in the tuple
    return top_k_items

def is_hit(top_k_items: list[dict], golden_item: dict, k:int) -> bool:
    top_k_urls = [url_entry["url"] for url_entry in top_k_items[:k]]
    expected_urls = golden_item["source_urls"]
    return bool(set(top_k_urls) & set(expected_urls)) #is_hit now compares two lists of urls (using set intersection) instead of one string, since source_urls in  golden set is a list ofmultiple correct answers.

'''
if __name__ == "__main__":

    # Chunk corpus befor model loop
    data_folder = Path("data")
    pages = load_pages(data_folder)
    children_with_urls = chunk_corpus(pages) 

    golden_set_path = Path(__file__).parent.parent / "eval" / "golden_set.json"
    golden_set_items = load_golden_set(golden_set_path)

    for model_name, embed_fn in EMBEDDING_MODELS.items():
        children_with_embeddings = embed_chunks(children_with_urls, embed_fn) #overwrites with next models embedding 
        hits_at_1 = 0
        hits_at_3 = 0

        for item in golden_set_items:
            question = item["question"]
            embedded_question = embed_question(question, embed_fn)
            top_k = retrieve_top_k(children_with_embeddings, embedded_question, 3)
            if is_hit(top_k, item, 1):
                hits_at_1 += 1
            if is_hit(top_k, item, 3):
                hits_at_3 += 1
        
        total = len(golden_set_items)
        print(f"{model_name}: hit@1 = {hits_at_1}/{total}, hit@3 = {hits_at_3}/{total}")
    
'''

def embed_with_openai_small(chunk: str) -> list[float]:
    #body just uses that alreafy crated client 
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk
    )
    return response.data[0].embedding

print(embed_with_openai_small("hello world")[:5])

'''
def embed_with_openai_large():

def embed_with_gemini_001():

def embed_with_cohere_v4():

def embed_with_voyagemultilingual_2():
'''





