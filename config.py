import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("PROXY_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://ai.api.cloud.yandex.net/v1")
MODEL = os.getenv("MODEL", "gpt://b1gajpa0fug3gnggb543/aliceai-llm/latest")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID", "b1gajpa0fug3gnggb543")

COMPETITORS = [
    "https://www.behance.net/",
    "https://dribbble.com/",
    "https://motionographer.com/",
]
