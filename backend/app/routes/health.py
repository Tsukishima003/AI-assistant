"""Health and readiness endpoints."""
from fastapi import APIRouter
from app.config.settings import settings
from app.services.document_service import get_document_count
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Real-Time RAG Assistant API",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@router.get("/health")
async def health_check():
    """Liveness check — returns healthy if app is up."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@router.get("/health/ready")
async def readiness_check():
    """
    Readiness check — verifies backend dependencies are reachable.
    Returns 503 if any dependency is unhealthy.
    """
    checks = {}

    # Check ChromaDB
    try:
        doc_count = get_document_count()
        checks["chromadb"] = {"status": "ok", "documents_indexed": doc_count}
    except Exception as e:
        logger.error("Readiness: ChromaDB check failed: %s", e)
        checks["chromadb"] = {"status": "error", "detail": str(e)}

    # Check Groq API key is configured
    groq_ok = bool(settings.GROQ_API_KEY and len(settings.GROQ_API_KEY) > 10)
    checks["groq_api"] = {"status": "ok" if groq_ok else "error"}

    all_ok = all(c["status"] == "ok" for c in checks.values())

    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={
            "status": "ready" if all_ok else "not_ready",
            "model": settings.GROQ_MODEL,
            "checks": checks,
        }
    )
