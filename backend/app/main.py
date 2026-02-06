"""FastAPI application entry point"""
import uvicorn
from fastapi import FastAPI
from app.config.settings import settings
from app.config.cors import setup_cors
from app.routes import health, documents, chat, websocket
from app.routes.websocket import router as websocket_router

app = FastAPI(title="Real-Time RAG Assistant API")

app.include_router(websocket_router)

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION
    )
    
    # Setup CORS
    setup_cors(app)
    
    # Include routers
    app.include_router(health.router)
    app.include_router(documents.router)
    app.include_router(chat.router)
    app.include_router(websocket.router)
    
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
