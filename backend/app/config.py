import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load your local environment keys automatically
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HISTORY_FILE = "translation_history.json"


if not GROQ_API_KEY:
    raise ValueError("System Missing Critical Secret Key: GROQ_API_KEY must be set in your .env environment.")

# Redirect standard traffic endpoints cleanly to Groq architecture
client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY #from .env file
)