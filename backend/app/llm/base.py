from abc import ABC, abstractmethod
from email import message
from typing import List, Dict, Any 

# Abstract base class jo hr llm provider follow kare ga 

class LLMClient(ABC):

    @abstractmethod
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Standard method format for generating LLM completions"""
        pass 

# Testing client jo static/scripted answers deta hai (No api needed)
class FakeClient(LLMClient):
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        last_message = messages[-1]["content"].lower() if messages else ""

        if "status" in last_message:
            return "Fake AI: your order is currently PENDING"
        elif "cancel" in last_message:
            return "Fake AI: Your order cancellation request has been logged"
        else:
            return "Fake AI: Hello! I am your Shopping Assistant. How can i help you today?"
        
