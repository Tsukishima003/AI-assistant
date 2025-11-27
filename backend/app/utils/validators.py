"""File validation utilities"""
from pathlib import Path
from typing import List


def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Validate if file extension is allowed
    
    Args:
        filename: Name of the file
        allowed_extensions: List of allowed extensions (e.g., ['.pdf', '.txt'])
    
    Returns:
        bool: True if valid, False otherwise
    """
    file_extension = Path(filename).suffix.lower()
    return file_extension in allowed_extensions


def validate_file_size(file_size_bytes: int, max_size_mb: int) -> bool:
    """
    Validate if file size is within limit
    
    Args:
        file_size_bytes: File size in bytes
        max_size_mb: Maximum allowed size in MB
    
    Returns:
        bool: True if valid, False otherwise
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_size_bytes <= max_size_bytes
