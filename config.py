import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def get_llm():
    """
    Create the LLM used by CareBridge.

    The API key and model name are loaded from
    environment variables and are never hard-coded.
    """

    api_key = os.getenv("LLM_API_KEY")
    model_name = os.getenv(
        "LLM_MODEL",
        "openai/gpt-oss-20b"
    )
    base_url = os.getenv(
        "LLM_BASE_URL",
        "https://openrouter.ai/api/v1"
    )

    if not api_key:
        raise ValueError(
            "LLM_API_KEY is not configured."
        )

    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url=base_url,
        temperature=0
    )
