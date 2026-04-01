"""Chat endpoint (non-streaming)."""
import uuid
from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import ChatMessage, ChatResponse
from app.services.document_service import query_documents
from app.core.rate_limiter import limiter

router = APIRouter(tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat(request: Request, message: ChatMessage):
    """Chat endpoint (non-streaming) with conversation memory and rate limiting."""
    try:
        result = query_documents(
            message.message,
            conversation_id=message.conversation_id
        )
        
        return ChatResponse(
            response=result['answer'],
            sources=result['sources'],
            conversation_id=result.get('conversation_id', message.conversation_id or str(uuid.uuid4()))
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
