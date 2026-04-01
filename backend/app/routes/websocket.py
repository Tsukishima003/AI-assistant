"""WebSocket endpoint for streaming chat."""
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.utils.websocket_manager import manager
from app.services.document_service import query_documents_stream, get_document_count
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time streaming chat"""
    await manager.connect(websocket)
    
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
                conversation_id = message_data.get("conversation_id")
                logger.info("Received question via WebSocket: %s (conv=%s)",
                          question[:100], conversation_id or "new")
                
                if not question:
                    await websocket.send_json({
                        "type": "error",
                        "content": "No message provided"
                    })
                    continue
                
                # Check if there are documents
                if get_document_count() == 0:
                    await websocket.send_json({
                        "type": "info",
                        "content": "No documents uploaded yet. Please upload documents first to use RAG features."
                    })
                    continue
                
                # Stream response with conversation memory
                async for chunk in query_documents_stream(question, conversation_id=conversation_id):
                    await websocket.send_json(chunk)
                
                logger.debug("Streaming complete, connection staying open")
                continue
                
            except json.JSONDecodeError as e:
                logger.warning("Invalid JSON received: %s", e)
                await websocket.send_json({
                    "type": "error",
                    "content": "Invalid message format"
                })
                continue
            
            except RuntimeError as e:
                if "disconnect" in str(e).lower():
                    logger.info("Client disconnected during message handling")
                    break
                else:
                    logger.error("Runtime error: %s", e)
                    continue
                
            except Exception as e:
                logger.error("Error processing WebSocket message: %s: %s",
                           type(e).__name__, str(e), exc_info=True)
                try:
                    await websocket.send_json({
                        "type": "error",
                        "content": f"Error: {str(e)}"
                    })
                except Exception:
                    pass
                continue
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    
    except Exception as e:
        logger.error("WebSocket fatal error: %s: %s",
                    type(e).__name__, str(e), exc_info=True)
        manager.disconnect(websocket)
