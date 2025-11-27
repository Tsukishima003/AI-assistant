"""LLM configuration for Groq"""
from langchain_groq import ChatGroq


def create_llm(api_key: str, model_name: str, temperature: float = 0.7, streaming: bool = True):
    """
    Create Groq LLM instance
    
    Args:
        api_key: Groq API key
        model_name: Model name (e.g., 'llama-3.1-70b-versatile')
        temperature: Temperature for generation
        streaming: Enable streaming
    
    Returns:
        ChatGroq: Configured LLM instance
    """
    return ChatGroq(
        groq_api_key=api_key,
        model_name=model_name,
        temperature=temperature,
        streaming=streaming
    )
