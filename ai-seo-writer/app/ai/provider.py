import os
import google.generativeai as genai
from abc import ABC, abstractmethod
from config.settings import Config

class BaseAIProvider(ABC):
    @abstractmethod
    def generate_content(self, prompt: str) -> str:
        pass

class GeminiProvider(BaseAIProvider):
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("Gemini API Key is missing. Please set GEMINI_API_KEY in .env file.")
        genai.configure(api_key=Config.GEMINI_API_KEY)
        # Using gemini-1.5-flash as the current standard model
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_content(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # We fail gracefully by re-raising with context
            raise Exception(f"Gemini API Error: {str(e)}")

def get_provider() -> BaseAIProvider:
    """Factory to get the configured AI provider"""
    # In the future, we can switch based on config
    return GeminiProvider()
