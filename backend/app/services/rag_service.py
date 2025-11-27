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
                # Local settings
                persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
                collection_name=settings.CHROMA_COLLECTION_NAME,
                # Cloud settings
                use_cloud=settings.CHROMA_USE_CLOUD,
                cloud_api_key=settings.CHROMA_CLOUD_API_KEY,
                cloud_tenant=settings.CHROMA_CLOUD_TENANT,
                cloud_database=settings.CHROMA_CLOUD_DATABASE,
                # Processing
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
