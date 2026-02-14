"""Text processing and chunking"""
from langchain.text_splitter import RecursiveCharacterTextSplitter


class TextProcessor:
    """Handles text splitting and chunking"""
    
    def __init__(self, chunk_size: int = 6000, chunk_overlap: int = 200):
        """
        Initialize text processor
        
        Args:
            chunk_size: Maximum size of each chunk
            chunk_overlap: Overlap between chunks
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n",".", " ", ""]
        )
    
    def split_documents(self, documents):
        """
        Split documents into chunks
        
        
        Args:
            documents: List of documents to split
        
        Returns:
            List: Chunked documents
        """
        return self.text_splitter.split_documents(documents)
