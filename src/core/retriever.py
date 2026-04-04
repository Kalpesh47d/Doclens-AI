import numpy as np
from sentence_transformers import SentenceTransformer
from src.config.constants import EMBEDDING_MODEL, DEFAULT_K
from src.core.vector_store import get_embedding_model

def retrieve(query, index, chunks, embeddings, k=DEFAULT_K):
    """Retrieve top-k relevant chunks for a query."""
    model = get_embedding_model()
    query_vec = model.encode([query])
    query_vec = query_vec / np.linalg.norm(query_vec, axis=1, keepdims=True)

    distances, indices = index.search(query_vec, k)

    results = []
    for i in indices[0]:
        results.append((chunks[i], i))

    return results
