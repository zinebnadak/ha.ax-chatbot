from dataclasses import dataclass 

@dataclass
class BotResponse:
    answer: str 
    retrieval_context: list[str] #chunks the pipeline retrieves this turn

def answer(question: str) -> BotResponse:
    # Just a stub rn. Wire into RAGPipeline.answer() later. Must return retrieval_context for the three metrics (not for answer relevancy) to work!
    raise NotImplementedError

