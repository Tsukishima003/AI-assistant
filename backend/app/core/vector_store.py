"""Vector store management using ChromaDB."""
import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List, Any
from app.core.logging import get_logger

logger = get_logger(__name__)


class VectorStore:

    def __init__(
        self,
        embeddings: Any,
        collection_name: str,
        persist_dir: str = "./chroma_db"
    ):
        self.collection_name = collection_name
        self.embeddings = embeddings
        self.persist_directory = persist_dir

        logger.info("Initializing local ChromaDB", extra={"persist_dir": persist_dir})
        try:
            self.chroma_client = chromadb.PersistentClient(path=persist_dir)
            logger.info("Local ChromaDB initialized successfully")
        except Exception as e:
            logger.error("ChromaDB initialization failed: %s", e, exc_info=True)
            raise

        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name
        )

        self.vector_store = Chroma(
            client=self.chroma_client,
            collection_name=collection_name,
            embedding_function=embeddings,
        )

    def add_documents(self, documents: List[Document]):
        return self.vector_store.add_documents(documents)

    def as_retriever(self, k: int = 4):
        return self.vector_store.as_retriever(search_kwargs={"k": k})

    def get_relevant_documents(self, query: str, k: int = 4) -> List[Document]:
        retriever = self.as_retriever(k=k)
        return retriever.invoke(query)

    def get_document_count(self) -> int:
        try:
            return self.collection.count()
        except Exception as e:
            logger.error("Error counting documents: %s", e)
            return 0

    def clear(self):
        try:
            logger.info("Clearing collection: %s", self.collection_name)
            self.chroma_client.delete_collection(self.collection_name)

            self.collection = self.chroma_client.get_or_create_collection(
                name=self.collection_name
            )

            self.vector_store = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings
            )
            logger.info("Collection cleared and re-initialized")
        except Exception as e:
            logger.error("Error clearing documents: %s", e, exc_info=True)