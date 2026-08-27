# BM25 is a keyword matching algorithm that ranks documents based on their relevance to a given query. 

from rank_bm25 import BM25Okapi
import re

def tokenize(text):
    return re.findall(r"\w+", text.lower()) # fixes punktuations 

corpus = [
    "The office is open Monday to Friday.",
    "Tuition fees are due at the start of each semester.",
    "Students can apply for financial aid online.",
    "The library closes at 9pm on weekdays.",
    "Office hours for academic advising are posted online.",
]

tokenized_corpus = [tokenize(sentence) for sentence in corpus]
print(tokenized_corpus)

query = "When is the office open?"
tokenized_query = tokenize(query)
print()
print(tokenized_query)

bm25 = BM25Okapi(tokenized_corpus)
scores = bm25.get_scores(tokenized_query)
print()
print(scores)
