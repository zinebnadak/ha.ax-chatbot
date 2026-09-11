'''
Run from package: uv run uvicorn app.main:app --reload

Then open a new terminal and run:
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Your question here!...", "language": "English"}'

or open: http://127.0.0.1:8000/docs

'''
from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.rag.pipeline import generate_answer
from app.guardrails.input_filters import filter_input
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()

# Rate-Limiting START
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# Rate-Limiting END

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-widget-url.onrender.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str
    language: str


@app.post("/chat")
@limiter.limit("7/minute")
async def chat(request: Request, chat_request: ChatRequest):

    # Validate and filter the input
    is_allowed, result = filter_input(chat_request.query, language=chat_request.language)
    if not is_allowed:
        return {"answer": result}

    # generate the answer using the RAG pipeline
    answer = generate_answer(
        query=chat_request.query,
        language=chat_request.language,
    )
    return {"answer": answer}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/docs")
def root():
    return {"message": "docs endpoint"}