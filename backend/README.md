# RAG Chat Backend - Modular Architecture

A clean, modular FastAPI backend with separated concerns for easy navigation and maintenance.

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # Application entry point
│   ├── config/
│   │   ├── settings.py      # Environment & configuration
│   │   └── cors.py          # CORS middleware
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   ├── routes/
│   │   ├── health.py        # Health & root endpoints
│   │   ├── documents.py     # Document CRUD
│   │   ├── chat.py          # Chat endpoint
│   │   └── websocket.py     # WebSocket streaming
│   ├── services/
│   │   ├── rag_service.py   # RAG engine wrapper
│   │   ├── file_service.py  # File operations
│   │   └── document_service.py # Document processing
│   └── utils/
│       ├── validators.py    # Validation utilities
│       └── websocket_manager.py # WebSocket manager
├── rag_engine.py            # Core RAG logic
├── models.py                # Legacy models (kept for reference)
├── main.py                  # Legacy main (kept for reference)
├── main_backup.py           # Backup of original
├── uploads/                 # Uploaded files
└── chroma_db/               # Vector database

```

## 🚀 Quick Start

```bash
# From backend directory
python app/main.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload --port 8000
```

## 📦 Module Overview

### Config Layer (`app/config/`)
- **settings.py**: Centralized configuration from environment variables
- **cors.py**: CORS middleware setup

### Models Layer (`app/models/`)
- **schemas.py**: Pydantic models for request/response validation

### Routes Layer (`app/routes/`)
- **health.py**: `/`, `/health`
- **documents.py**: `/upload`, `/documents/count`, `/documents` (DELETE)
- **chat.py**: `/chat` (POST)
- **websocket.py**: `/ws/chat` (WebSocket)

### Services Layer (`app/services/`)
- **rag_service.py**: Singleton wrapper for RAG engine
- **file_service.py**: File upload/validation/storage
- **document_service.py**: Document processing and RAG operations

### Utils Layer (`app/utils/`)
- **validators.py**: File validation utilities
- **websocket_manager.py**: WebSocket connection management

## 🔍 Navigation Guide

**Want to...**

- **Add a new endpoint?** → `app/routes/`
- **Change configuration?** → `app/config/settings.py`
- **Modify business logic?** → `app/services/`
- **Add validation?** → `app/utils/validators.py`
- **Update request/response models?** → `app/models/schemas.py`

## 🧪 Testing

Test endpoints:
```bash
# Health check
curl http://localhost:8000/health

# Upload document
curl -X POST -F "file=@document.pdf" http://localhost:8000/upload

# Document count
curl http://localhost:8000/documents/count
```

## 📝 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Architecture Benefits

### ✅ Separation of Concerns
- Routes handle HTTP/WebSocket
- Services contain business logic
- Config centralizes settings
- Utils provide reusable functions

### ✅ Easy Navigation
- Clear file organization
- Logical module structure
- Find code by functionality

### ✅ Better Testability
- Test modules independently
- Mock dependencies easily
- Clear interfaces

### ✅ Scalability
- Easy to add new routes
- Simple to extend services
- Clear patterns

## 🔄 Migration from Old Structure

The old monolithic `main.py` has been refactored into:
- **Routes**: 4 files (health, documents, chat, websocket)
- **Services**: 3 files (rag, file, document)
- **Config**: 2 files (settings, cors)
- **Utils**: 2 files (validators, websocket_manager)
- **Models**: 1 file (schemas)

Original files kept as backups:
- `main_backup.py` - Original main.py
- `models.py` - Original models (now in app/models/schemas.py)

## 🛠️ Development

The application uses:
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **LangChain** - RAG framework
- **ChromaDB** - Vector database
- **Groq** - LLM provider

## 🗄️ ChromaDB Architecture

This application uses **ChromaDB in HTTP Server Mode** - ChromaDB runs as a separate Docker service that your backend connects to via HTTP.

**Architecture:**
```
┌─────────────┐         ┌──────────────┐
│   FastAPI   │ ────────▶│  ChromaDB    │
│  Backend    │  HTTP    │   Server     │
│  (Port 8001)│         │  (Port 8000) │
└─────────────┘         └──────────────┘
```

**Benefits:**
- **Scalability**: ChromaDB scales independently from backend
- **Resource Isolation**: Backend crashes don't affect ChromaDB
- **Data Persistence**: Vectors stored in Docker volume
- **Zero-Downtime Updates**: Update backend without losing vectors

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Edit .env and add your GROQ_API_KEY
nano .env

# 3. Start all services
docker compose up -d

# 4. Check service health
curl http://localhost:8001/health
curl http://localhost:8000/api/v1/heartbeat
```

### Service Architecture

```yaml
services:
  chromadb:    # Vector database server
    - Port: 8000
    - Volume: chroma_data
    
  backend:     # FastAPI application
    - Port: 8001 → 8000
    - Depends on: chromadb
```

### Docker Commands

```bash
# View logs
docker compose logs -f backend
docker compose logs -f chromadb

# Restart backend only
docker compose restart backend

# Rebuild and restart
docker compose up -d --build

# Check status
docker compose ps

# Stop all services
docker compose down

# Stop and remove volumes (⚠️ deletes data)
docker compose down -v
```

---

## 📋 Environment Variables

Create a `.env` file (use `.env.example` as template):

```env
# ChromaDB Server Configuration
CHROMA_SERVER_HOST=chromadb
CHROMA_SERVER_PORT=8000
CHROMA_COLLECTION_NAME=documents

# Groq AI Configuration (REQUIRED)
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

---

## 🚀 Quick Start Guide

### Production Deployment (with Docker)

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env: Add your GROQ_API_KEY

# 2. Start services
docker compose up -d

# 3. Verify deployment
curl http://localhost:8001/health
```

### Local Development (without Docker)

**Note**: For local development, you still need ChromaDB server running.

```bash
# 1. Start ChromaDB server separately
docker run -p 8000:8000 chromadb/chroma:latest

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env: Set CHROMA_SERVER_HOST=localhost

# 4. Run the application
python app/main.py
# OR
uvicorn app.main:app --reload --port 8001
```

## 📚 Code Examples

### Adding a New Route

Create `app/routes/new_feature.py`:
```python
from fastapi import APIRouter

router = APIRouter(tags=["New Feature"])

@router.get("/new-endpoint")
async def new_endpoint():
    return {"message": "Hello"}
```

Then add to `app/main.py`:
```python
from app.routes import health, documents, chat, websocket, new_feature

app.include_router(new_feature.router)
```

### Adding a New Service

Create `app/services/new_service.py`:
```python
def do_something():
    """Service function"""
    return "result"
```

Use in routes:
```python
from app.services.new_service import do_something

@router.get("/endpoint")
async def endpoint():
    result = do_something()
    return {"result": result}
```

---

**Clean, modular, and easy to navigate!** 🎉
