"""Pydantic models for request/response validation"""
from pydantic import BaseModel
from typing import List, Optional


class ChatMessage(BaseModel):
    """Chat message model"""
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    sources: List[str] = []
    conversation_id: str


class DocumentUploadResponse(BaseModel):
    """Document upload response model"""
    filename: str
    status: str
    chunks_created: int
    message: str


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
