import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.config.constants import EMBEDDING_MODEL

# Cache model to load only once
_model_cache = None

def get_embedding_model():
    global _model_cache
    if _model_cache is None:
        _model_cache = SentenceTransformer(EMBEDDING_MODEL)
    return _model_cache

def create_vector_store(chunks):
    model = get_embedding_model()
    embeddings = model.encode(chunks)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index, embeddings, chunks
