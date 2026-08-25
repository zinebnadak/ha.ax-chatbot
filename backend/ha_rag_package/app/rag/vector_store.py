import chromadb
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]  # count up to ha.ax-chatbot/
DATABASE_PATH = PROJECT_ROOT / "backend" / "chroma_db"

client = chromadb.PersistentClient(path=str(DATABASE_PATH))

COLLECTION_NAME = "ha_rag_collection"

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}  # Chroma's default is L2, not cosine — match what we evaluated with
)


print('Collection name:', collection.name)
print('Collection count:', collection.count())
print('Metadata:', collection.metadata)