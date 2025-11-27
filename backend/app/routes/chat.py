"""Chat endpoint (non-streaming)"""
import uuid
from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatMessage, ChatResponse
from app.services.document_service import query_documents

router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Chat endpoint (non-streaming)"""
    try:
        result = query_documents(message.message)
        
        return ChatResponse(
            response=result['answer'],
            sources=result['sources'],
            conversation_id=message.conversation_id or str(uuid.uuid4())
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
