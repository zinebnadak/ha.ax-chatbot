'''
Flow: 
1. pre-embed the corpus once per model (cache to disk so repeat runs are free)
2. loop on terminal input for a question index
3. print all models answers and compare retrieval quality, or compare each models top-k (k *number of chunks most similar to the query) OR just use a similarity threshold

Models I will be comparing:

'''
