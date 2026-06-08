
# core/embedding.py

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_embedding(text: str):
    """
    Convert text → vector embedding
    """
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",  # or groq-supported embedding model
            input=text
        )
        return response.data[0].embedding

    except Exception as e:
        return None