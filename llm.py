import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

MODEL = "llama-3.3-70b-versatile"

def get_answer(context_chunks, query):
    print(type(context_chunks))
    print(type(context_chunks[0]))
    context = "\n".join([str(c) for c in context_chunks])

    prompt = f"""
You are an intelligent assistant.

Use ONLY the provided context to answer.
If answer is not found, say "Not found in document".

Context:
{context}

Question:
{query}

Answer:
"""

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()["choices"][0]["message"]["content"]