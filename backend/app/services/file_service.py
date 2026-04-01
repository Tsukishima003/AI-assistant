"""File service - Handle file upload, validation, and storage."""
import re
from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.config.settings import settings
from app.utils.validators import validate_file_extension, validate_file_size
from app.core.logging import get_logger

logger = get_logger(__name__)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and other attacks.
    
    - Strips directory components (e.g. ../../etc/passwd → passwd)
    - Removes non-alphanumeric chars except dots, hyphens, underscores
    - Limits length to 255 chars
    """
    # Take only the basename (strip any directory path)
    name = Path(filename).name

    # Remove any characters that aren't alphanumeric, dots, hyphens, underscores, or spaces
    name = re.sub(r'[^\w\s\-.]', '', name)

    # Collapse multiple dots/spaces
    name = re.sub(r'\.{2,}', '.', name)
    name = re.sub(r'\s+', '_', name)

    # Limit length
    name = name[:255]

    if not name or name.startswith('.'):
        name = f"upload_{name}"

    return name


async def save_uploaded_file(file: UploadFile) -> Path:
    """
    Save uploaded file to disk with validation.
    
    Args:
        file: Uploaded file
    
    Returns:
        Path: Path to saved file
    
    Raises:
        HTTPException: If file type or size not valid
    """
    # Validate file type
    if not validate_file_extension(file.filename, settings.ALLOWED_FILE_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed: {settings.ALLOWED_FILE_EXTENSIONS}"
        )

    # Read content and validate size
    content = await file.read()

    if not validate_file_size(len(content), settings.MAX_FILE_SIZE_MB):
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE_MB}MB"
        )

    # Sanitize filename
    safe_name = sanitize_filename(file.filename)
    file_path = settings.UPLOAD_DIRECTORY / safe_name
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    logger.info("File saved: %s (%d bytes, original: %s)", safe_name, len(content), file.filename)
    return file_path


def delete_file(file_path: Path) -> bool:
    """
    Delete file from disk.
    
    Args:
        file_path: Path to file
    
    Returns:
        bool: True if deleted, False otherwise
    """
    try:
        if file_path.exists():
            file_path.unlink()
            logger.info("File deleted: %s", file_path)
            return True
        return False
    except Exception as e:
        logger.error("Error deleting file %s: %s", file_path, e)
        return False
