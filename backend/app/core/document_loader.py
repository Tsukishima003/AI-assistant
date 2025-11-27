"""Document loading utilities"""
from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader


def load_document(file_path: str) -> List:
    """
    Load a document based on file extension
    
    Args:
        file_path: Path to document file
    
    Returns:
        List: Loaded documents
    
    Raises:
        ValueError: If file type not supported
    """
    file_extension = Path(file_path).suffix.lower()
    
    if file_extension == '.pdf':
        loader = PyPDFLoader(file_path)
    elif file_extension == '.txt':
        loader = TextLoader(file_path)
    elif file_extension in ['.docx', '.doc']:
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")
    
    return loader.load()
