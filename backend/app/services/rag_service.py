"""RAG service - Wrapper for RAG engine with singleton pattern"""
from app.core.rag_engine import RAGEngine
from app.config.settings import settings


class RAGService:
    """Singleton wrapper for RAG Engine"""
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> RAGEngine:
        """Get or create RAG Engine instance"""
        if cls._instance is None:
            cls._instance = RAGEngine(
                groq_api_key=settings.GROQ_API_KEY,
                model_name=settings.GROQ_MODEL,
                collection_name=settings.CHROMA_COLLECTION_NAME,
                persist_dir=settings.CHROMA_PERSIST_DIR,
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP
            )
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance (useful for testing)"""
        cls._instance = None


# Global RAG service instance
rag_service = RAGService.get_instance()
