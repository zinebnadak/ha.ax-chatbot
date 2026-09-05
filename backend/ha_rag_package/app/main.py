# cmd run from package: uv run uvicorn app.main:app --reload

from fastapi import FastAPI
from pydantic import BaseModel
from app.rag.pipeline import generate_answer

app = FastAPI()

class ChatRequest(BaseModel):
    query: str  
    language: str
    is_first_message: bool = False

@app.post("/chat")
async def chat(request: ChatRequest):
    answer = generate_answer(
        query=request.query,
        language=request.language,
        is_first_message=request.is_first_message,
    )
    return {"answer": answer}

@app.get("/health")
async def health_check():
    return{"status": "healthy"}

@app.get("/docs")
def root():
    return {"message": "docs endpoint"}

