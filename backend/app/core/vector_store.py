"""Vector store operations using ChromaDB Cloud"""
import chromadb
from langchain_community.vectorstores import Chroma


class VectorStore:
    """Manages ChromaDB vector store operations via Chroma Cloud"""
    
    def __init__(
        self, 
        embeddings,
        collection_name: str,
        cloud_api_key: str,
        cloud_tenant: str,
        cloud_database: str = "RRAG"
    ):
        """
        Initialize vector store with Chroma Cloud client
        
        Args:
            embeddings: Embedding function
            collection_name: Name of the collection
            cloud_api_key: Chroma Cloud API key
            cloud_tenant: Chroma Cloud tenant ID
            cloud_database: Chroma Cloud database name
        """
        self.collection_name = collection_name
        self.embeddings = embeddings
        
        # Initialize ChromaDB Cloud client
        print(f"🌐 Connecting to Chroma Cloud: {cloud_tenant}/{cloud_database}")
        try:
            # Use CloudClient for Chroma Cloud (chromadb >= 1.0)
            self.chroma_client = chromadb.CloudClient(
                tenant=cloud_tenant,
                database=cloud_database,
                api_key=cloud_api_key
            )
            # Test connection
            self.chroma_client.heartbeat()
            print("✅ Connected to Chroma Cloud successfully!")
        except Exception as e:
            print(f"❌ Chroma Cloud connection failed: {e}")
            print(f"💡 Tip: Check your API key, tenant, and database settings")
            raise
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name
        )
        
        # Initialize LangChain vector store wrapper
        self.vector_store = Chroma(
            client=self.chroma_client,
            collection_name=collection_name,
            embedding_function=embeddings
        )
    
    def add_documents(self, documents):
        """Add documents to vector store"""
        self.vector_store.add_documents(documents)
    
    def as_retriever(self, k: int = 4):
        """Get retriever for similarity search"""
        return self.vector_store.as_retriever(search_kwargs={"k": k})
    
    def get_relevant_documents(self, query: str, k: int = 4):
        """Get relevant documents for a query"""
        retriever = self.as_retriever(k=k)
        return retriever.get_relevant_documents(query)
    
    def get_document_count(self) -> int:
        """Get number of documents in vector store"""
        try:
            return self.collection.count()
        except:
            return 0
    
    def clear(self):
        """Clear all documents from vector store"""
        try:
            self.chroma_client.delete_collection(self.collection_name)
            self.collection = self.chroma_client.get_or_create_collection(
                name=self.collection_name
            )
            self.vector_store = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings
            )
        except Exception as e:
            print(f"Error clearing documents: {e}")
