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


def add_chunks_to_db(chunks: list[dict]) -> None: # Each chunk dict needs: id, text, embedding, url, title, lang
    collection.add(
        ids=[c["id"] for c in chunks],
        embeddings=[c["embedding"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[
            {"url": c["url"], "title": c["title"], "lang": c["lang"]}
            for c in chunks
        ],
    )

def reset_collection() -> None:
    global collection
    client.delete_collection(COLLECTION_NAME)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

def query_db(query_embedding: list[float], k: int = 5) -> list[dict]:
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    chunk_hits = []
    
    for i in range(len(results["ids"][0])):
        chunk_hits.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "url": results["metadatas"][0][i]["url"],
                "title": results["metadatas"][0][i]["title"],
                "lang": results["metadatas"][0][i]["lang"],
                "distance": results["distances"][0][i]
        })
    return chunk_hits


if __name__ == "__main__":
    from embeddings import embed_documents, embed_query

    reset_collection()

    test_chunks = [
        {"id": "1", "text": "The office is open Monday to Friday.", "url": "https://example.com/hours", "title": "Office Hours", "lang": "en"},
        {"id": "2", "text": "Tuition fees are due at the start of each semester.", "url": "https://example.com/fees", "title": "Tuition", "lang": "en"},
    ]

    embeddings = embed_documents([c["text"] for c in test_chunks])
    for chunk, embedding in zip(test_chunks, embeddings):
        chunk["embedding"] = embedding

    add_chunks_to_db(test_chunks)

    print("count in collection:", collection.count())  # debug line

    query_embedding = embed_query("When is the office open?")
    results = query_db(query_embedding, k=2)

    print("number of results:", len(results))  # debug line

    for r in results:
        print(round(r["distance"], 4), "-", r["title"], "-", r["url"])