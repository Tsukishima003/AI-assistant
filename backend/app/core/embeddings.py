"""Embedding model configuration"""
from langchain_community.embeddings import HuggingFaceEmbeddings


def create_embeddings():
    """
    Create embedding model for document vectorization
    
    Returns:
        HuggingFaceEmbeddings: Embedding model instance
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
