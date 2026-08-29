# BM25 is a keyword matching algorithm that ranks documents based on their relevance to a given query. 
# RRF sidesteps the scale-mismatch problems of BM25 and Dense retrieval by combining their scores in a reciprocal manner., both sides share the chunk id.

from rank_bm25 import BM25Okapi
import re
from pathlib import Path
from vector_store import collection
from embeddings import embed_query
from vector_store import query_db


# Chroma's collection already store "text "for every chunk

PROJECT_ROOT = Path(__file__).resolve().parents[4] # index 3 to go four levels up from the file itself
DATABASE_FOLDER = PROJECT_ROOT / "backend" / "chroma_db"

result = collection.get(include=["documents", "metadatas"])
print(len(result["ids"]))  # number of chunks in the collection

def tokenize(text):
    return re.findall(r"\w+", text.lower()) # fixes punktuations 

tokenized_corpus = [tokenize(sentence) for sentence in result["documents"]]

query = "When is the office open?"
tokenized_query = tokenize(query)

bm25 = BM25Okapi(tokenized_corpus)
scores = bm25.get_scores(tokenized_query)

top_n = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:3]

'''
#BM25 results
for i in top_n:
    print(round(scores[i], 4), "-", result["documents"][i])
'''

#Dense retrieval results
query_embedding = embed_query(query)
dense_results = query_db(query_embedding, k=20)
# print(dense_results)

dense_ranked_ids = [item['id'] for item in dense_results]

def reciprocal_rank_fusion(bm25_ranked_ids, dense_ranked_ids, k=60):
    scores = {}

    for rank, doc_id in enumerate(bm25_ranked_ids):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)

    for rank, doc_id in enumerate(dense_ranked_ids):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


bm25_ranked_ids = [result["ids"][i] for i in top_n]
fused = reciprocal_rank_fusion(bm25_ranked_ids, dense_ranked_ids)
for doc_id, score in fused:
    print(round(score, 4), "-", doc_id)