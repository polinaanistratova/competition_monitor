import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("PROXY_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
MODEL = os.getenv("MODEL", "gpt-4o-mini")

COMPETITORS = [
    "https://www.behance.net/",
    "https://dribbble.com/",
    "https://motionographer.com/",
]
