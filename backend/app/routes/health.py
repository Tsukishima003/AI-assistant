"""Health and root endpoints"""
from fastapi import APIRouter
from app.config.settings import settings
from app.services.document_service import get_document_count

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Real-Time RAG Assistant API",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    doc_count = get_document_count()
    return {
        "status": "healthy",
        "documents_indexed": doc_count,
        "model": settings.GROQ_MODEL
    }
