
from app.guardrails.system_prompt import build_system_prompt
from app.rag.retrieval import retrieve_with_context
from openai import OpenAI

client = OpenAI()

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

'''
This function builds the RAG prompt by retrieving context based on the user's query, 
formatting it, and then constructing the system prompt.
'''
def build_rag_prompt(query: str, language: str, is_first_message: bool = False) -> str:
    hits = retrieve_with_context(query)
    context = format_retrieved_context(hits)

    return build_system_prompt(
        context=context,
        language=language,
        is_first_message=is_first_message,
    )

'''
This function generates an answer to the user's query by building the RAG prompt
,then using the OpenAI API to get a response.
'''

def generate_answer(query: str, language: str, is_first_message: bool = False) -> str:
    system_prompt = build_rag_prompt(
        query=query,
        language=language,
        is_first_message=is_first_message,
    )

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=system_prompt,
        input=query,
    )

    return response.output_text


