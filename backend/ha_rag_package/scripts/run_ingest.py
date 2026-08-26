# run as a module using (ha-rag-package) zizo@zizos-MacBook-Air ha_rag_package % python3 -m scripts.run_ingest

from pathlib import Path
from app.rag.chunking import load_pages, chunk_all_pages #using Path as input to load_pages() and then chunk_all_pages() 
from app.rag.embeddings import embed_documents
from app.rag.vector_store import add_chunks_to_db, reset_collection

def enrich_children(children: list[dict], parents: list[dict]) -> list[dict]:# enrich with url, title, lang and later embeddings because add_chunks_to_db() needs them
    parent_dict = {parent["id"]: parent for parent in parents}
    
    for child in children:
        parent = parent_dict[child["parent_id"]]
        child["url"] = parent["url"]
        child["title"] = parent["title"]
        child["lang"] = parent["lang"]
    
    return children

def main(): 
    PROJECT_ROOT = Path(__file__).resolve().parents[3] # index 3 to go four levels up from the file itself
    data_folder = PROJECT_ROOT / "data"
    pages = load_pages(data_folder)
    parents, children = chunk_all_pages(pages)

    # debug line: print(f"pages: {len(pages)}, parents: {len(parents)}, children: {len(children)}")

    children = enrich_children(children, parents)

    texts = [child["text"] for child in children]
    embeddings = embed_documents(texts)

    for child, embedding in zip(children, embeddings):
        child["embedding"] = embedding
    
    reset_collection()
    add_chunks_to_db(children)

    # debug line: from app.rag.vector_store import collection
    # debug line: print("count in collection:", collection.count())

if __name__ == "__main__":
    main()
