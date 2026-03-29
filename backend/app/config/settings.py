import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator

class Settings(BaseSettings):
    # API Info
    APP_TITLE: str = "Real-Time RAG Assistant API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI Assistant with RAG using Groq Llama and Chroma Cloud"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Groq AI
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    # --- CHROMA CLOUD ONLY ---
    CHROMA_PERSIST_DIR:str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "documents"
    
    # Document Processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # File Upload
    UPLOAD_DIRECTORY: Path = Field(default=Path("./uploads"))
    ALLOWED_FILE_EXTENSIONS: list[str] = ['.pdf', '.txt', '.docx', '.doc']
    MAX_FILE_SIZE_MB: int = 50

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

    @model_validator(mode='after')
    def confirm_cloud_config(self) -> 'Settings':
        print(f".")
        return self

settings = Settings()
settings.UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)