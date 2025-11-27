"""Document service - Document processing and RAG operations"""
from app.services.rag_service import rag_service


def process_document(file_path: str) -> int:
    """
    Process document and add to vector store
    
    Args:
        file_path: Path to document
    
    Returns:
        int: Number of chunks created
    """
    return rag_service.process_document(file_path)


def get_document_count() -> int:
    """
    Get count of indexed documents
    
    Returns:
        int: Number of documents
    """
    return rag_service.get_document_count()


def clear_all_documents():
    """Clear all documents from vector store"""
    rag_service.clear_documents()


async def query_documents_stream(question: str):
    """
    Query documents with streaming response
    
    Args:
        question: User question
    
    Yields:
        Dict: Streaming response chunks
    """
    async for chunk in rag_service.query_stream(question):
        yield chunk


def query_documents(question: str) -> dict:
    """
    Query documents (non-streaming)
    
    Args:
        question: User question
    
    Returns:
        dict: Answer and sources
    """
    return rag_service.query(question)
