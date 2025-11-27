import os
import json
import uuid
from pathlib import Path
from typing import List

from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from models import ChatMessage, ChatResponse, DocumentUploadResponse, ErrorResponse
from rag_engine import RAGEngine

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Real-Time RAG Assistant API",
    description="AI Assistant with RAG using Groq Llama and ChromaDB",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Engine
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

rag_engine = RAGEngine(
    groq_api_key=GROQ_API_KEY,
    model_name=os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"),
    persist_directory=os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db"),
    collection_name=os.getenv("CHROMA_COLLECTION_NAME", "documents"),
    chunk_size=int(os.getenv("CHUNK_SIZE", 1000)),
    chunk_overlap=int(os.getenv("CHUNK_OVERLAP", 200))
)

# Create uploads directory
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Store active WebSocket connections
active_connections: List[WebSocket] = []


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Real-Time RAG Assistant API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    doc_count = rag_engine.get_document_count()
    return {
        "status": "healthy",
        "documents_indexed": doc_count,
        "model": os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
    }


@app.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.txt', '.docx', '.doc']
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_extension} not supported. Allowed: {allowed_extensions}"
            )
        
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process document
        chunks_created = rag_engine.process_document(str(file_path))
        
        return DocumentUploadResponse(
            filename=file.filename,
            status="success",
            chunks_created=chunks_created,
            message=f"Document processed successfully. Created {chunks_created} chunks."
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Chat endpoint (non-streaming)"""
    try:
        result = rag_engine.query(message.message)
        
        return ChatResponse(
            response=result['answer'],
            sources=result['sources'],
            conversation_id=message.conversation_id or str(uuid.uuid4())
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time streaming chat"""
    await websocket.accept()
    active_connections.append(websocket)
    print(f"WebSocket connected. Total connections: {len(active_connections)}")
    
    try:
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Handle heartbeat ping
                if message_data.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
                    continue
                
                question = message_data.get("message", "")
                print(f"Received question: {question}")
                
                if not question:
                    await websocket.send_json({
                        "type": "error",
                        "content": "No message provided"
                    })
                    continue
                
                # Check if there are documents
                if rag_engine.get_document_count() == 0:
                    await websocket.send_json({
                        "type": "info",
                        "content": "No documents uploaded yet. Please upload documents first to use RAG features."
                    })
                    continue
                
                # Stream response
                async for chunk in rag_engine.query_stream(question):
                    await websocket.send_json(chunk)
                
                # Send a keepalive ping to prevent connection closure
                print("Streaming complete, connection staying open for next message...")
                
                # Explicitly continue the loop to wait for next message
                continue
                
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                await websocket.send_json({
                    "type": "error",
                    "content": "Invalid message format"
                })
                continue
            
            except RuntimeError as e:
                # This happens when the client has disconnected
                if "disconnect" in str(e).lower():
                    print(f"Client disconnected during message handling")
                    break  # Exit the while loop
                else:
                    print(f"Runtime error: {e}")
                    continue
                
            except Exception as e:
                print(f"Error processing message: {type(e).__name__}: {str(e)}")
                import traceback
                traceback.print_exc()
                try:
                    await websocket.send_json({
                        "type": "error",
                        "content": f"Error: {str(e)}"
                    })
                except:
                    pass
                # Don't break the loop, continue waiting for next message
                continue
    
    except WebSocketDisconnect:
        if websocket in active_connections:
            active_connections.remove(websocket)
        print(f"Client disconnected. Remaining connections: {len(active_connections)}")
    
    except Exception as e:
        print(f"WebSocket fatal error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        if websocket in active_connections:
            active_connections.remove(websocket)


@app.delete("/documents")
async def clear_documents():
    """Clear all documents from the vector store"""
    try:
        rag_engine.clear_documents()
        return {"status": "success", "message": "All documents cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents/count")
async def get_document_count():
    """Get count of indexed documents"""
    count = rag_engine.get_document_count()
    return {"count": count}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
