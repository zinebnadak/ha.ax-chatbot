# cmd: uv run fastapi dev /Users/zizo/ha.ax-chatbot/backend/app/main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    return{"status": "healthy"}

@app.get("/docs")
def root():
    return {"message": "docs endpoint"}

