"""Exception handlers for FastAPI HTTPExceptions and validation errors."""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.logging import get_logger

logger = get_logger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTPExceptions with consistent format."""
    logger.warning(
        "HTTP %d on %s %s: %s",
        exc.status_code, request.method, request.url.path, exc.detail
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "detail": None,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors with readable messages."""
    errors = exc.errors()
    logger.warning(
        "Validation error on %s %s: %s",
        request.method, request.url.path, errors
    )
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "detail": [
                {
                    "field": " -> ".join(str(loc) for loc in e.get("loc", [])),
                    "message": e.get("msg", ""),
                }
                for e in errors
            ],
        },
    )
