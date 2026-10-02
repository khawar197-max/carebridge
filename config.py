import os

import streamlit as st
from langchain_openai import ChatOpenAI


def get_secret(name: str, default=None):
    """
    Read a secret from Streamlit Secrets first,
    then fall back to environment variables.
    """

    try:
        value = st.secrets.get(name)

        if value:
            return value

    except Exception:
        pass

    return os.getenv(name, default)


def get_llm():
    """
    Create the Groq LLM used by CareBridge.
    """

    api_key = get_secret("GROQ_API_KEY")

    model_name = get_secret(
        "GROQ_MODEL",
        "openai/gpt-oss-20b"
    )

    base_url = "https://api.groq.com/openai/v1"

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured."
        )

    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url=base_url,
        temperature=0
    )
