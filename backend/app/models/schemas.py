"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field
from typing import List, Optional


class ChatMessage(BaseModel):
    """Chat message model with validation."""
    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="User message (1-10000 chars)"
    )
    conversation_id: Optional[str] = Field(
        default=None,
        max_length=64,
        description="Conversation ID for memory tracking"
    )


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    sources: List[str] = []
    conversation_id: str


class DocumentUploadResponse(BaseModel):
    """Document upload response model."""
    filename: str
    status: str
    chunks_created: int
    message: str


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None
