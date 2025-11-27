"""CORS middleware configuration"""
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app):
    """Configure CORS middleware for the FastAPI application"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify exact origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
