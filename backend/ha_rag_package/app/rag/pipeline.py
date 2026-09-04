
from app.guardrails.system_prompt import build_system_prompt

'''
This Function formats the retrieved context into a string that can be included in the system prompt. 
It takes a list of hits (retrieved documents) and returns 
- A formatted string that includes the source URL, title, and text of each hit. 
- If there are no hits, it returns a message indicating that there is no retrieved context.
'''

def format_retrieved_context(hits: list[dict]) -> str:
    if not hits:
        return "NO RETRIEVED CONTEXT."

    parts = []

    for i, hit in enumerate(hits, start=1):
        parts.append(
            f"""SOURCE {i}
source_url: {hit["url"]}
title: {hit["title"]}

{hit["text"]}"""
        )

    return "\n\n---\n\n".join(parts)


Then pipeline.py supplies:
is_first_message=True