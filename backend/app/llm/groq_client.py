import os
from typing import List, Dict
from groq import Groq
from app.llm.base import LLMClient

class GroqClient(LLMClient):
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing in environment variables.")
        self.client = Groq(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content