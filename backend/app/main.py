"""FastAPI application entry point."""
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.config.settings import settings
from app.config.cors import setup_cors
from app.routes import health, documents, chat, websocket
from app.core.logging import setup_logging, get_logger, generate_request_id, request_id_var
from app.core.rate_limiter import limiter
from app.middleware import ExceptionMiddleware
from app.middleware.exceptions import http_exception_handler, validation_exception_handler

# Initialize logging BEFORE anything else
setup_logging(settings.LOG_LEVEL)
logger = get_logger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Injects a unique request ID into every request for log tracing."""

    async def dispatch(self, request: Request, call_next):
        rid = generate_request_id()
        request_id_var.set(rid)
        request.state.request_id = rid

        logger.info("%s %s", request.method, request.url.path)
        response = await call_next(request)
        response.headers["X-Request-ID"] = rid
        return response


async def _rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Return 429 with a JSON body when rate limit is exceeded."""
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=429,
        content={"error": "Rate limit exceeded", "detail": str(exc.detail)},
    )


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION
    )

    # Rate limiter state
    app.state.limiter = limiter

    # Middleware (order matters — outermost first)
    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(ExceptionMiddleware)
    app.add_middleware(RequestIdMiddleware)

    # Setup CORS
    setup_cors(app)

    # Exception handlers
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(RateLimitExceeded, _rate_limit_handler)

    # Include routers
    app.include_router(health.router)
    app.include_router(documents.router)
    app.include_router(chat.router)
    app.include_router(websocket.router)

    logger.info(
        "App created | env=%s | model=%s",
        settings.ENVIRONMENT, settings.GROQ_MODEL
    )
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )