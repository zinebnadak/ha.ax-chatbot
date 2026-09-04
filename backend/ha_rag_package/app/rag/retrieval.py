# BM25 is a keyword matching algorithm that ranks documents based on their relevance to a given query. 
# RRF sidesteps the scale-mismatch problems of BM25 and Dense retrieval by combining their scores in a reciprocal manner., both sides share the chunk id.

from rank_bm25 import BM25Okapi
import re
import json
from pathlib import Path
from .vector_store import collection
from .embeddings import embed_query
from .vector_store import query_db


# Chroma's collection already store "text "for every chunk

PROJECT_ROOT = Path(__file__).resolve().parents[4] # index 3 to go four levels up from the file itself
DATABASE_FOLDER = PROJECT_ROOT / "backend" / "chroma_db"


def tokenize(text):
    return re.findall(r"\w+", text.lower())  # fixes punktuations


def reciprocal_rank_fusion(bm25_ranked_ids, dense_ranked_ids, k=60):
    scores = {}

    for rank, doc_id in enumerate(bm25_ranked_ids):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)

    for rank, doc_id in enumerate(dense_ranked_ids):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


# module-level cache so we don't rebuild the BM25 index on every call
_bm25_cache = None
_result_cache = None


def _get_corpus():
    global _bm25_cache, _result_cache
    if _bm25_cache is None:
        result = collection.get(include=["documents", "metadatas"])
        print(len(result["ids"]))  # number of chunks in the collection

        tokenized_corpus = [tokenize(sentence) for sentence in result["documents"]]
        _bm25_cache = BM25Okapi(tokenized_corpus)
        _result_cache = result
    return _bm25_cache, _result_cache


def retrieve(query: str, bm25_top_n: int = 3, dense_k: int = 20):
    bm25, result = _get_corpus()

    tokenized_query = tokenize(query)
    scores = bm25.get_scores(tokenized_query)

    top_n = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:bm25_top_n]

    '''
    #BM25 results
    for i in top_n:
        print(round(scores[i], 4), "-", result["documents"][i])
    '''

    # Dense retrieval results
    query_embedding = embed_query(query)
    dense_results = query_db(query_embedding, k=dense_k)
    # print(dense_results)

    dense_ranked_ids = [item['id'] for item in dense_results]

    bm25_ranked_ids = [result["ids"][i] for i in top_n]
    fused = reciprocal_rank_fusion(bm25_ranked_ids, dense_ranked_ids)
    return fused


# --- parent expansion: map a child chunk hit back to its full parent text ---

PARENTS_PATH = Path(__file__).resolve().parent / "parents.json"
_parents_cache = None


def _load_parents():
    global _parents_cache
    if _parents_cache is None:
        with open(PARENTS_PATH, "r", encoding="utf-8") as f:
            parents = json.load(f)
        _parents_cache = {p["id"]: p for p in parents}
    return _parents_cache


def retrieve_with_context(query: str, k: int = 5, bm25_top_n: int = 3, dense_k: int = 20):
    fused = retrieve(query, bm25_top_n=bm25_top_n, dense_k=dense_k)
    parents = _load_parents()

    hits = []
    seen_parents = set()
    for child_id, score in fused:
        parent_id = child_id.rsplit("_child-", 1)[0]
        if parent_id in seen_parents:
            continue
        parent = parents.get(parent_id)
        if parent:
            hits.append({
                "child_id": child_id,
                "score": score,
                "text": parent["text"],
                "url": parent["url"],
                "title": parent["title"],
            })
            seen_parents.add(parent_id)
        if len(hits) >= k:
            break
    return hits


if __name__ == "__main__":
    query = "When is the office open?"
    fused = retrieve(query)
    for doc_id, score in fused:
        print(round(score, 4), "-", doc_id)