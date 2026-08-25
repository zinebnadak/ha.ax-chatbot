from openai import OpenAI 
import os 
from dotenv import load_dotenv
from pathlib import Path 

PROJECT_ROOT = Path(__file__).resolve().parents[4]  # count up to ha.ax-chatbot/
load_dotenv(PROJECT_ROOT / ".env")

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
embedding_model = "text-embedding-3-small"


def embed_documents(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model=embedding_model, input=texts)
    return [item.embedding for item in response.data]



if __name__ == "__main__":
    documents = embed_documents(["doc one", "doc two", "doc three"])
    print("documents size:", len(documents), "each length:", len(documents[0]))