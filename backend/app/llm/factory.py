import os
from app.llm.base import LLMClient, FakeClient
from app.llm.groq_client import GroqClient

def get_llm_client() -> LLMClient:
    # .env se provider read karein (default: 'fake')
    provider = os.getenv("LLM_PROVIDER", "fake").lower()
    
    if provider == "fake":
        return FakeClient()
    elif provider == "groq":
        return GroqClient()
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")