"""File service - Handle file upload, validation, and storage"""
from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.config.settings import settings
from app.utils.validators import validate_file_extension


async def save_uploaded_file(file: UploadFile) -> Path:
    """
    Save uploaded file to disk
    
    Args:
        file: Uploaded file
    
    Returns:
        Path: Path to saved file
    
    Raises:
        HTTPException: If file type not supported
    """
    # Validate file type
    if not validate_file_extension(file.filename, settings.ALLOWED_FILE_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed: {settings.ALLOWED_FILE_EXTENSIONS}"
        )
    
    # Save file
    file_path = settings.UPLOAD_DIRECTORY / file.filename
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return file_path


def delete_file(file_path: Path) -> bool:
    """
    Delete file from disk
    
    Args:
        file_path: Path to file
    
    Returns:
        bool: True if deleted, False otherwise
    """
    try:
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
        return False
