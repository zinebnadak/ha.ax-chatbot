# Högskolan på Åland — AI Chatbot Widget

## What it does
A production ready RAG-powered chatbot that answers questions about programmes and admissions at [ha.ax](https://www.ha.ax/), based on the university's own website content

> This repository contains a revised version of the original ha.ax chatbot demo, incorporating stakeholder feedback and architectural improvements. The original demo repository can be found here: [ha.ax-chatbot-demo](https://github.com/zinebnadak/ha.ax-chatbot-demo.git).

## Architecture

1. **Ingest**: Scraper → Chunking (parent/child) → Embeddings → ChromaDB
2. **Retrieve**: User question → Hybrid retrieval (BM25 + dense + RRF) → parent-chunk expansion
3. **Generate**: System prompt + context → GPT-4o-mini → guardrails (injection, moderation, rate limiting) → answer

### ha_rag_package
The RAG chatbot backend

## Tech stack
Python Language · FastAPI · ChromaDB · OpenAI (embeddings + GPT-4o-mini) · BeautifulSoup · rank_bm25 · Vite/vanilla JS · Langfuse · slowapi · Render

## Running cost estimate

| Item | Cost |
|------|------|
| OpenAI embeddings (one-time ingest) | ~$0.01 |
| GPT-4o-mini per query | ~$0.001 |
| 100 queries/day | ~$0.45/month |
| Render — widget (static site) | Free |
| Render — backend (free tier) | Free (cold starts after inactivity) |
| Render — backend (Starter, always-on) | $7/month |
| **Total estimated monthly cost** | **~$0.50/month (free tier) to ~$7.50/month (always-on)** |

## Live deployment
- Frontend widget (Vite static site) on Render: [https://ha-ax-chatbot-widget.onrender.com](https://ha-ax-chatbot-widget.onrender.com)
- Backend (FastAPI) on Render: [https://ha-ax-chatbot.onrender.com/docs](https://ha-ax-chatbot.onrender.com/docs)

<img src="docs/images/fastapi.png" width="300">

*Note: Render's free tier spins down after inactivity, causing a ~30-60s delay on the first request after idle time.*

## Screenshots

**Launcher (closed state)**

<img src="docs/images/widget_launcher.png" width="250">

**Greeting (Swedish and English)**

<img src="docs/images/swe_widget.png" width="280"> <img src="docs/images/eng_widget.png" width="280">

**Guardrails**

<img src="docs/images/guardrails.png" width="300">

**Answering a question with citation**

<img src="docs/images/citation.png" width="300">

## Local setup
### backend
```
cd backend/ha_rag_package
uv sync
uv run uvicorn app.main:app --reload
```

### widget
```
cd widget
npm install
npm run dev
```


## Known limitations on this version
> This is the second, rebuilt version of the project, not a finished product. It's meaningfully more solid than the first prototype (real guardrails, rate limiting, citations, a working widget), but it still has gaps, listed honestly below. Some are quick fixes, others (like cross-lingual retrieval) need more work than a month allowed. Its built and shipped with that understood.

- Broad "what programmes do you offer" questions sometimes list only one programme instead of all.
- EASE master's programme (English-only source) is sometimes missed by Swedish questions.
- No conversation memory — each message is answered independently.
- "Without a diploma" questions don't always mention real alternative pathways that exist on the site.
- Occasionally cites a stale/contradictory source page instead of the correct one.

## Handoff
See [DEPLOY.md](DEPLOY.md) how I made step-by-step deployment instructions for ha.ax IT staff.

---
Made by Zineb Nadak

