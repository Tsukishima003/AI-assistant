"""Document management endpoints"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import DocumentUploadResponse
from app.services.file_service import save_uploaded_file
from app.services.document_service import process_document, get_document_count, clear_all_documents

router = APIRouter(prefix="", tags=["Documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Save file
        file_path = await save_uploaded_file(file)
        
        # Process document
        chunks_created = process_document(str(file_path))
        
        return DocumentUploadResponse(
            filename=file.filename,
            status="success",
            chunks_created=chunks_created,
            message=f"Document processed successfully. Created {chunks_created} chunks."
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents/count")
async def document_count():
    """Get count of indexed documents"""
    count = get_document_count()
    return {"count": count}


@router.delete("/documents")
async def clear_documents():
    """Clear all documents from the vector store"""
    try:
        clear_all_documents()
        return {"status": "success", "message": "All documents cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
