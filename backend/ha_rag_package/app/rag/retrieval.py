# BM25 is a keyword matching algorithm that ranks documents based on their relevance to a given query. 

from rank_bm25 import BM25Okapi
import re
from pathlib import Path
from vector_store import collection


# Chroma's collection already store "text "for every chunk

PROJECT_ROOT = Path(__file__).resolve().parents[4] # index 3 to go four levels up from the file itself
DATABASE_FOLDER = PROJECT_ROOT / "backend" / "chroma_db"

result = collection.get(include=["documents", "metadatas"])
print(len(result["ids"]))  # number of chunks in the collection

def tokenize(text):
    return re.findall(r"\w+", text.lower()) # fixes punktuations 

tokenized_corpus = [tokenize(sentence) for sentence in result["documents"]]
print(tokenized_corpus)

'''
query = "When is the office open?"
tokenized_query = tokenize(query)
print()
print(tokenized_query)

bm25 = BM25Okapi(tokenized_corpus)
scores = bm25.get_scores(tokenized_query)
print()
print(scores)
'''

