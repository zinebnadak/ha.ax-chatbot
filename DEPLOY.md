# DEPLOY.md (Draft)

Instructions targeted toward IT staff looking to evaluating deployment. Written after a working Render-based deployment or for any actual hosting choice.

## What this is
Two separate services:
1. **Backend** — FastAPI app (retrieval + AI generation + guardrails)
2. **Widget** — static JS chat widget, embeddable on any web-page

## Backend deployment
- Python 3.13, managed with `uv`
- Requires: `OPENAI_API_KEY` (required), `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` (optional, for observability)
- Includes a pre-built ChromaDB vector database (`backend/chroma_db/`, ~12MB). Must be deployed alongside the code, not regenerated on every deploy
- Start command: `uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Exposes: `POST /chat`, `GET /health`

## Widget deployment
- Static site (Vite build): `npm install && npm run build` → deploy the `dist/` folder
- Before building, update `API_URL` in `src/main.js` to point at the deployed backend URL if provider changed

## Required before going live
- [ ] Set real CORS origin on backend (currently locked to one widget URL, so update if domain changes)
- [ ] Re-run `run_ingest.py` if source website content has changed since last scrape
- [ ] Decide on a real domain/subdomain for both services
- [ ] Review or change rate limit (`15/minute` per IP) against expected real traffic


## Not covered here
Actual domain/SSL setup, monitoring/alerting, scaling — depends on chosen host.