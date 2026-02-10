import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Info
    APP_TITLE: str = "Real-Time RAG Assistant API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI Assistant with RAG using Groq Llama and ChromaDB"
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Groq AI
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    if not GROQ_API_KEY:
    
        raise ValueError("key not found")
    
    # ChromaDB Configuration
    # Mode selection: HTTP Server > Cloud > Local (in priority order)
    CHROMA_USE_HTTP: bool = os.getenv("CHROMA_USE_HTTP", "false").lower() == "true"
    CHROMA_USE_CLOUD: bool = os.getenv("CHROMA_USE_CLOUD", "false").lower() == "true"
    
    # HTTP Server mode settings (recommended for production)
    CHROMA_SERVER_HOST: str = os.getenv("CHROMA_SERVER_HOST", "chromadb")
    CHROMA_SERVER_PORT: int = int(os.getenv("CHROMA_SERVER_PORT", 8000))
    
    # Chroma Cloud settings
    CHROMA_CLOUD_API_KEY: str = os.getenv("CHROMA_CLOUD_API_KEY", "")
    CHROMA_CLOUD_TENANT: str = os.getenv("CHROMA_CLOUD_TENANT", "")
    CHROMA_CLOUD_DATABASE: str = os.getenv("CHROMA_CLOUD_DATABASE", "RRAG")
    
    # Local ChromaDB settings (fallback for development)
    CHROMA_PERSIST_DIRECTORY: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "../database")
    CHROMA_COLLECTION_NAME: str = os.getenv("CHROMA_COLLECTION_NAME", "documents")
    
    # Document Processing
    CHUNK_SIZE: int = int(1000)
    CHUNK_OVERLAP: int = int(200)
    
    # File Upload
    UPLOAD_DIRECTORY: Path = Path("./uploads")
    ALLOWED_FILE_EXTENSIONS: list = ['.pdf', '.txt', '.docx', '.doc']
    MAX_FILE_SIZE_MB: int = 50


# Create settings instance
settings = Settings()

# Validate critical settings
if not settings.GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# Validate ChromaDB configuration based on mode
if settings.CHROMA_USE_HTTP:
    print(f"ChromaDB HTTP Server mode: {settings.CHROMA_SERVER_HOST}:{settings.CHROMA_SERVER_PORT}")
elif settings.CHROMA_USE_CLOUD:
    if not settings.CHROMA_CLOUD_API_KEY or not settings.CHROMA_CLOUD_TENANT:
        raise ValueError("CHROMA_CLOUD_API_KEY and CHROMA_CLOUD_TENANT required when CHROMA_USE_CLOUD=true")
    print(f"Chroma Cloud enabled: {settings.CHROMA_CLOUD_TENANT}/{settings.CHROMA_CLOUD_DATABASE}")
else:
    print(f"Local ChromaDB: {settings.CHROMA_PERSIST_DIRECTORY}")

# Ensure upload directory exists
settings.UPLOAD_DIRECTORY.mkdir(exist_ok=True)
