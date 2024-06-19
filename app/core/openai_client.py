import openai
from .config import settings

# Set your OpenAI API key
if not settings.openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set")

openai.api_key = settings.openai_api_key
