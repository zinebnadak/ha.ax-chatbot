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



