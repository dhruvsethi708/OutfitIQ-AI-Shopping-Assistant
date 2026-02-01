from pathlib import Path
import toml
import os
import google.generativeai as genai

# Load config
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "config.toml"
config = toml.load(CONFIG_PATH)

# ENV first (Render-safe)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or config.get("geminiai", {}).get("api_key")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)


class LLMInvoke:
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL_NAME)

    def llm_response(self, query, context):
        prompt = f"""
You are a helpful AI fashion assistant.

Use ONLY the information provided in the context.
If wardrobe items are missing, suggest reasonable clothing types.

Context:
{context}

User Query:
{query}

Answer in clean HTML using <ul> and <li>.
"""

        try:
            response = self.model.generate_content(prompt)

            # Safe extraction
            if hasattr(response, "text") and response.text:
                return {"answer": response.text}

            if response.candidates:
                parts = response.candidates[0].content.parts
                if parts and hasattr(parts[0], "text"):
                    return {"answer": parts[0].text}

            return {"answer": "<ul><li>No recommendation available.</li></ul>"}

        except Exception as e:
            print("Gemini LLM Error:", e)
            return {
                "answer": "<ul><li>AI recommendation is temporarily unavailable.</li></ul>"
            }
