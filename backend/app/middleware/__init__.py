"""Global exception handling middleware."""
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import get_logger

logger = get_logger(__name__)


class ExceptionMiddleware(BaseHTTPMiddleware):
    """Catches unhandled exceptions and returns a consistent JSON error response."""

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            logger.error(
                "Unhandled exception on %s %s: %s",
                request.method,
                request.url.path,
                exc,
                exc_info=True,
            )
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "detail": str(exc) if _is_debug(request) else None,
                },
            )


def _is_debug(request: Request) -> bool:
    """Only expose error details in non-production environments."""
    try:
        from app.config.settings import settings
        return settings.ENVIRONMENT != "production"
    except Exception:
        return False
