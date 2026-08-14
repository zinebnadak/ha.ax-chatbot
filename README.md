# Högskolan på Åland — AI Chatbot 

A production ready RAG-powered chatbot that answers questions about programmes and admissions at [ha.ax](https://www.ha.ax/), based on the university's own website content

> This repository contains a revised version of the original ha.ax chatbot demo, incorporating stakeholder feedback and architectural improvements. The original demo repository can be found here: [ha.ax-chatbot-demo](https://github.com/zinebnadak/ha.ax-chatbot-demo.git)

Public preview (Streamlit Community Cloud): [link]()

---

# ha_rag_package
The RAG chatbot backend.

---

## Running cost estimate

| Item | Cost |
|------|------|
| OpenAI embeddings (one-time ingest) | ~$0.01 |
| GPT-4o-mini per query | ~$0.001 |
| 100 queries/day | ~$0.45/month |
| Streamlit Community Cloud | Free |
| Railway (production alternative) | ~$5/month |
| **Total estimated monthly cost** | **~$5-10/month** |

---

## Handoff
See [DEPLOY.md](/docs/DEPLOY.md) how I made step-by-step deployment instructions for ha.ax IT staff.

Made by Zineb Nadak

