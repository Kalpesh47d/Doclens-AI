import requests
import os
from dotenv import load_dotenv
from src.config.constants import LLM_MODEL, LLM_TEMPERATURE, LLM_API_ENDPOINT

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

def get_answer(context_chunks, query):
    """Generate answer from LLM using context chunks and query."""
    context = "\n".join([str(c) for c in context_chunks])

    prompt = f"""You are an intelligent assistant.

Use ONLY the provided context to answer.
If answer is not found, say "Not found in document".

Context:
{context}

Question:
{query}

Answer:
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": LLM_TEMPERATURE
    }

    response = requests.post(LLM_API_ENDPOINT, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]
