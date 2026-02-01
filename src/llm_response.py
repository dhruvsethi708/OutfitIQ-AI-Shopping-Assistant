from pathlib import Path
import toml
from google import genai
import os

# Load config
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "config.toml"
config = toml.load(CONFIG_PATH)


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Create Gemini client (NEW API)
client = genai.Client(api_key=GEMINI_API_KEY)


class LLMInvoke:
    def llm_response(self, query, context):
        prompt = f"""
You are a helpful AI fashion assistant.

Use ONLY the information provided in the context.
If wardrobe items are missing, suggest reasonable clothing types.

Context:
{context}

User Query:
{query}

Answer strictly in clean HTML using <ul> and <li>.
"""

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )

            if response and response.text:
                return {"answer": response.text}

            return {
                "answer": "<ul><li>No outfit recommendation available.</li></ul>"
            }

        except Exception as e:
            print("Gemini LLM Error:", e)
            return {
                "answer": "<ul><li>AI recommendation is temporarily unavailable.</li></ul>"
            }
