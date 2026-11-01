import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()

if PROVIDER == "openrouter":
    from langchain_openai import ChatOpenAI
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set.")
    
    llm = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL", "google/gemma-4-31b-it:free"),
    temperature=0,
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )
    
else:
    from langchain_ollama import ChatOllama

    llm = ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
        temperature=0
    )