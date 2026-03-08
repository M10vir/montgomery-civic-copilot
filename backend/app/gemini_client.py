import os
from typing import Optional

from google import genai
from google.genai import types

from .config import GEMINI_API_KEY

DEFAULT_MODEL = "gemini-3-flash-preview"  # fast + cheap, great for hackathon MVP

class GeminiClient:
    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_MODEL):
        key = api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        if not key:
            raise ValueError("GEMINI_API_KEY is missing. Set it in .env")
        self.client = genai.Client(api_key=key)
        self.model = model

    def generate(self, prompt: str) -> str:
        resp = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=700,
            ),
        )
        # resp.text is the simplest output
        return (resp.text or "").strip()
