from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.models.schemas import DocumentUploadResponse
from app.services.file_service import save_uploaded_file
from app.services.document_service import process_document, get_document_count, clear_all_documents

router = APIRouter(prefix="", tags=["Documents"])

# Track processing status
processing_status: dict = {}

def process_in_background(file_path: str, filename: str):
    """Background task to process document"""
    try:
        processing_status[filename] = {"status": "processing", "chunks": 0}
        chunks_created = process_document(str(file_path))
        processing_status[filename] = {"status": "success", "chunks": chunks_created}
    except Exception as e:
        processing_status[filename] = {"status": "error", "error": str(e)}


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Upload document and process in background"""
    try:
        file_path = await save_uploaded_file(file)
        processing_status[file.filename] = {"status": "processing", "chunks": 0}
        background_tasks.add_task(process_in_background, str(file_path), file.filename)

        return DocumentUploadResponse(
            filename=file.filename,
            status="processing",
            chunks_created=0,
            message="File uploaded, processing in background..."
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents/status/{filename}")
async def document_status(filename: str):
    """Poll processing status of a document"""
    status = processing_status.get(filename, {"status": "unknown"})
    return status


@router.get("/documents/count")
async def document_count():
    count = get_document_count()
    return {"count": count}


@router.delete("/documents")
async def clear_documents():
    try:
        clear_all_documents()
        processing_status.clear()
        return {"status": "success", "message": "All documents cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))