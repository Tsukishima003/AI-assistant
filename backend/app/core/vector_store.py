"""Vector store operations using ChromaDB (local or cloud)"""
import chromadb
from langchain_community.vectorstores import Chroma


class VectorStore:
    """Manages ChromaDB vector store operations (supports local and cloud)"""
    
    def __init__(
        self, 
        embeddings,
        collection_name: str,
        # Local mode params
        persist_directory: str = None,
        # Cloud mode params
        use_cloud: bool = False,
        cloud_api_key: str = None,
        cloud_tenant: str = None,
        cloud_database: str = "RAG"
    ):
        """
        Initialize vector store
        
        Args:
            embeddings: Embedding function
            collection_name: Name of the collection
            persist_directory: Directory for local storage (local mode)
            use_cloud: Whether to use Chroma Cloud
            cloud_api_key: Chroma Cloud API key
            cloud_tenant: Chroma Cloud tenant ID
            cloud_database: Chroma Cloud database name
        """
        self.collection_name = collection_name
        self.embeddings = embeddings
        self.use_cloud = use_cloud
        
        # Initialize ChromaDB client (cloud or local)
        if use_cloud:
            print(f"🌐 Connecting to Chroma Cloud: {cloud_tenant}/{cloud_database}")
            try:
                # Use CloudClient for Chroma Cloud
                self.chroma_client = chromadb.CloudClient(
                    api_key=cloud_api_key,
                    tenant=cloud_tenant,
                    database=cloud_database
                )
                print("✅ Connected to Chroma Cloud successfully!")
            except Exception as e:
                print(f"❌ Chroma Cloud connection failed: {e}")
                print("💡 Tip: Verify your API key and tenant in Chroma Cloud dashboard")
                raise
        else:
            print(f"💾 Using local ChromaDB: {persist_directory}")
            self.chroma_client = chromadb.PersistentClient(path=persist_directory)
        
        # Initialize vector store
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
            collection = self.chroma_client.get_collection(self.collection_name)
            return collection.count()
        except:
            return 0
    
    def clear(self):
        """Clear all documents from vector store"""
        try:
            self.chroma_client.delete_collection(self.collection_name)
            self.vector_store = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings
            )
        except Exception as e:
            print(f"Error clearing documents: {e}")
