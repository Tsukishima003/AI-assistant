"""Document service - Document processing and RAG operations."""
from typing import Optional
from app.services.rag_service import rag_service
from app.core.conversation import conversation_manager


def process_document(file_path: str) -> int:
    """
    Process document and add to vector store.
    
    Args:
        file_path: Path to document
    
    Returns:
        int: Number of chunks created
    """
    return rag_service.process_document(file_path)


def get_document_count() -> int:
    """
    Get count of indexed documents.
    
    Returns:
        int: Number of documents
    """
    return rag_service.get_document_count()


def clear_all_documents():
    """Clear all documents from vector store."""
    rag_service.clear_documents()


async def query_documents_stream(question: str, conversation_id: Optional[str] = None):
    """
    Query documents with streaming response and conversation memory.
    
    Args:
        question: User question
        conversation_id: Optional conversation ID for history tracking
    
    Yields:
        Dict: Streaming response chunks
    """
    # Get or create conversation
    conv = conversation_manager.get_or_create(conversation_id)
    conv.add_user_message(question)
    chat_history = conv.get_history_text()

    # Yield the established conversation_id first so the client can reuse it
    yield {"type": "conversation_id", "content": conv.id}

    full_response = ""
    async for chunk in rag_service.query_stream(question, chat_history=chat_history):
        if chunk.get("type") == "done":
            full_response = chunk.get("content", "")
        yield chunk

    # Save assistant response to history
    if full_response:
        conv.add_assistant_message(full_response)


def query_documents(question: str, conversation_id: Optional[str] = None) -> dict:
    """
    Query documents (non-streaming) with conversation memory.
    
    Args:
        question: User question
        conversation_id: Optional conversation ID for history tracking
    
    Returns:
        dict: Answer, sources, and conversation_id
    """
    conv = conversation_manager.get_or_create(conversation_id)
    conv.add_user_message(question)
    chat_history = conv.get_history_text()

    result = rag_service.query(question, chat_history=chat_history)

    # Save assistant response to history
    conv.add_assistant_message(result["answer"])

    result["conversation_id"] = conv.id
    return result
