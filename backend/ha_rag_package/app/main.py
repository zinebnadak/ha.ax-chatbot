'''
Run from package: uv run uvicorn app.main:app --reload

Then open a new terminal and run:
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Your question here!...", "language": "English"}'

or open: http://127.0.0.1:8000/docs

'''

from fastapi import FastAPI
from pydantic import BaseModel
from app.rag.pipeline import generate_answer
from app.guardrails.input_filters import filter_input
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str  
    language: str

@app.post("/chat")
async def chat(request: ChatRequest):

    # Validate and filter the input
    is_allowed, result = filter_input(request.query, language=request.language)
    if not is_allowed:
        return {"answer": result}

    # generate the answer using the RAG pipeline
    answer = generate_answer(
        query=request.query,
        language=request.language,
    )
    return {"answer": answer}

@app.get("/health")
async def health_check():
    return{"status": "healthy"}

@app.get("/docs")
def root():
    return {"message": "docs endpoint"}