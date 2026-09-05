'''
This function will be used in the answering pipeline. 
If the answer is empty or None it returns a fallback contact message instead or jnoting
'''

def filter_output(answer: str) -> str:
    if not answer:
        return "I don´t have that information - please contact info@ha.ax or +358 (0)18 537 000."

    return answer.strip()