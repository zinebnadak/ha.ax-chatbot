from openai import OpenAI 
import os 
from dotenv import load_dotenv
from pathlib import Path 

PROJECT_ROOT = Path(__file__).resolve().parents[4]  # count up to ha.ax-chatbot/
load_dotenv(PROJECT_ROOT / ".env")

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


if __name__ == "__main__":
    print("PROJECT_ROOT:", PROJECT_ROOT)
    response = client.embeddings.create(model="text-embedding-3-small", input="hello world")
    embedding = response.data[0].embedding
    print("length:", len(embedding))
    print("first 5:", embedding[:5])


