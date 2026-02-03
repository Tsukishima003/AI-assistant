# Real-Time AI Assistant with RAG and LangChain

A modern, real-time AI assistant powered by **Retrieval-Augmented Generation (RAG)** using **Groq Llama** and **ChromaDB**. Chat with your documents and get intelligent, context-aware answers with beautiful streaming responses.

## Features

- **Groq Llama Integration** - Lightning-fast responses using Groq's LLM API
- **RAG Pipeline** - Intelligent document retrieval with semantic search
- **ChromaDB Vector Store** - Persistent local vector database
- **Real-Time Streaming** - Watch responses appear token-by-token via WebSocket
- **Multi-Format Support** - Upload PDF, DOCX, and TXT documents
- **Premium UI** - Dark mode with glassmorphism and smooth animations
- **Responsive Design** - Works seamlessly on desktop and mobile
- **Source Citations** - See which documents informed each answer

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com))

### Installation

1. **Clone or navigate to the project directory**
```powershell  
cd "c:\Users\DELL\Documents\RAG LC"
```

2. **Install Python dependencies**
```powershell
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the project root:
```powershell
Copy-Item .env.example .env
```

Edit `.env` and add your Groq API key:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

### Running the Application

1. **Start the backend server**
```powershell
cd backend
python main.py
```

The server will start at `http://localhost:8000`

2. **Open the frontend**

Open `frontend/index.html` in your web browser, or use a simple HTTP server:
```powershell
cd frontend
python -m http.server 3000
```

Then navigate to `http://localhost:3000`

## 📖 Usage Guide

### 1. Upload Documents

- Click the upload area or drag-and-drop files
- Supported formats: PDF, TXT, DOCX
- Documents are automatically processed and indexed

### 2. Chat with Your Documents

- Type your question in the input box
- Press Enter or click the send button
- Watch the AI response stream in real-time
- View source documents for each answer

### 3. Manage Documents

- See document count in the sidebar
- Click "Clear All" to remove all documents
- 
### Components

- **Frontend**: HTML5, CSS3, Vanilla JavaScript with WebSocket
- **Backend**: FastAPI with async/await support
- **LLM**: Groq Llama (llama-3.1-70b-versatile)
- **Embeddings**: HuggingFace sentence-transformers
- **Vector Store**: ChromaDB with persistent storage
- **Document Processing**: PyPDF2, python-docx

## 🔧 Configuration

Edit `.env` to customize:

```env
# Model selection
GROQ_MODEL=llama-3.1-70b-versatile
# Other options: llama-3.1-8b-instant, mixtral-8x7b-32768

# Server settings
HOST=0.0.0.0
PORT=8000

# ChromaDB settings
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=documents

# Document processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## Project Structure

```
RAG LC/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── rag_engine.py        # RAG pipeline implementation
│   └── models.py            # Pydantic data models
├── frontend/
│   ├── index.html           # Main HTML structure
│   ├── styles.css           # Premium dark mode styling
│   └── app.js               # WebSocket & UI logic
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## API Endpoints

### REST API

- `GET /` - Root endpoint with API info
- `GET /health` - Health check and stats
- `POST /upload` - Upload document
- `POST /chat` - Non-streaming chat (alternative to WebSocket)
- `GET /documents/count` - Get indexed document count
- `DELETE /documents` - Clear all documents

### WebSocket

- `WS /ws/chat` - Real-time streaming chat

## UI Features

- **Dark Mode**: Eye-friendly dark theme
- **Glassmorphism**: Modern translucent panels
- **Smooth Animations**: Micro-interactions throughout
- **Typing Indicators**: Visual feedback while AI is thinking
- **Auto-scroll**: Messages automatically scroll into view
- **Toast Notifications**: Elegant status messages
- **Drag-and-Drop**: Easy document uploads

## Security Notes

This is a development setup. For production:

- Use environment-specific CORS origins
- Add authentication/authorization
- Implement rate limiting
- Use HTTPS/WSS protocols
- Validate and sanitize all inputs
- Add file upload size limits

## Troubleshooting

**WebSocket connection fails:**
- Ensure backend is running on port 8000
- Check if another service is using the port
- Verify firewall settings

**Document upload fails:**
- Check file format (PDF, TXT, DOCX only)
- Ensure file is not corrupted
- Check backend logs for errors

**No responses from AI:**
- Verify GROQ_API_KEY is set correctly
- Check if documents are uploaded
- Monitor backend console for errors

## License

MIT License - feel free to use for personal or commercial projects.

## Contributing

Contributions welcome! Feel free to submit issues or pull requests.
