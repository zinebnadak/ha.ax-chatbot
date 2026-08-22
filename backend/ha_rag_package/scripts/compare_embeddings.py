"""
Compare embedding retrieval quality against a golden set.

Metrics:
- Recall@1
- Recall@3

Flow:
1. Load and chunk the corpus.
2. Embed the corpus once per model.
3. Embed each golden-set question.
4. Retrieve the most similar chunks.
5. Compare retrieved URLs against the golden-set source URLs.

(Cache to disk when you'd otherwise re-run the same model's embedding step more than once, e.g retrieve_top_k/is_hit logic without wanting to re-embed the corpus each time you test a change.)

Models:
- text-embedding-3-small
- text-embedding-3-large
- cohere´s embed v4.0
- voyage_3_large
- gemini-embedding-001

Run:
    uv run backend/ha_rag_package/scripts/compare_embeddings.py
"""

from pathlib import Path 
import json
from ha_rag_package.app.rag.chunking import chunk_all_pages, load_pages
from typing import Callable
import numpy as np
import time

import os
from dotenv import load_dotenv
from openai import OpenAI
from google import genai
import cohere
import voyageai

# load environment variables and create client instances once. 
PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")

openai_client = OpenAI()
cohere_client = cohere.ClientV2(api_key=os.environ["COHERE_API_KEY"])
voyageai_client = voyageai.Client(api_key=os.environ["VOYAGE_API_KEY"])
gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Golden set
def load_golden_set(file_path: Path) -> list[dict]:
    with file_path.open("r", encoding="utf-8") as file:
        golden_set_file = json.load(file)

        return [
            item for item in golden_set_file
            if item.get("source_urls")
        ]

# Corpus
def chunk_corpus(pages: list[dict]) -> list[dict]:
    parents, children = chunk_all_pages(pages)

    lookup_dict = {} # tool to attach urls
    for item in parents:
        lookup_dict[item["id"]] = item["url"] # adds/updates one key

    # modifying each child dict by adding a "url" key into it
    for item in children:
        item["url"] = lookup_dict[item["parent_id"]]

    return children

# Embedding (should do ONE job)
def embed_chunks (children: list[dict], embedding_fn: Callable[[str], list[float]] ) -> list[dict]: 
    for item in children:
        item["embedding"] = embedding_fn(item["text"]) # fn returns list[float] eg. the embedding 
    
    return children

def embed_question(question: str, embedding_fn: Callable) -> list[float]:
    try:
        return embedding_fn(question, is_query=True)
    except TypeError:
        return embedding_fn(question)

# Similarity / retrieval
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

# Evaluation
def is_hit(top_k_items: list[dict], golden_item: dict, k:int) -> bool:
    top_k_urls = [url_entry["url"] for url_entry in top_k_items[:k]]
    expected_urls = golden_item["source_urls"]
    return bool(set(top_k_urls) & set(expected_urls)) #is_hit now compares two lists of urls (using set intersection) instead of one string, since source_urls in  golden set is a list ofmultiple correct answers.

# Models 

'''
def embed_with_openai_small(chunk: str) -> list[float]:
    #body just uses that already created client 
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=chunk
    )
    return response.data[0].embedding


def embed_with_openai_large(chunk: str) -> list[float]:
    response = openai_client.embeddings.create(
        model="text-embedding-3-large",
        input=chunk
    )
    return response.data[0].embedding


def embed_with_cohere_v4(chunk: str, is_query: bool = False) -> list[float]:
    input_type = "search_query" if is_query else "search_document"
    response = cohere_client.embed(
        model="embed-v4.0", texts=[chunk], input_type=input_type,
        output_dimension=1024, embedding_types=["float"]
    )
    time.sleep(0.7)
    return response.embeddings.float[0]

def embed_with_voyage_3_large(chunk: str, is_query: bool = False) -> list[float]:
    input_type = "query" if is_query else "document"
    result = voyageai_client.embed(
        [chunk], 
        model="voyage-3-large", 
        input_type=input_type)
    return result.embeddings[0]

'''

def embed_with_gemini_001(chunk: str) -> list[float]:
    result = gemini_client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunk
    )
    return result.embeddings[0].values

EMBEDDING_MODELS = {
    #"text-embedding-3-small": embed_with_openai_small,
    #"text-embedding-3-large": embed_with_openai_large,
    #"cohere-embed-v4": embed_with_cohere_v4,
    #"voyage-3-large": embed_with_voyage_3_large,
    "google-gemini-embeddings-001": embed_with_gemini_001   # only one model active, uncommented to test others
}

# Main
if __name__ == "__main__":

    # Chunk corpus before model loop
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



