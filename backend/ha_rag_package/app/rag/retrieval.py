# BM25 is a keyword matching algorithm that ranks documents based on their relevance to a given query. 

from rank_bm25 import BM25Okapi
import re
from pathlib import Path
from vector_store import collection
from embeddings import embed_query
from vecor_store import query_db


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

for i in top_n:
    print(round(scores[i], 4), "-", result["documents"][i])


