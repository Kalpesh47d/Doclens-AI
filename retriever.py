import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def retrieve(query, index, chunks, embeddings, k=3):
    query_vec = model.encode([query])
    query_vec = query_vec / np.linalg.norm(query_vec, axis=1, keepdims=True)

    distances, indices = index.search(query_vec, k)

    results = []
    for i in indices[0]:
        results.append((chunks[i], i))

    return results