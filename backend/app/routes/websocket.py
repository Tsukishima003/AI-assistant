"""WebSocket endpoint for streaming chat"""
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.utils.websocket_manager import manager
from app.services.document_service import query_documents_stream, get_document_count

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
                print(f"Received question: {question}")
                
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
                
                # Stream response
                async for chunk in query_documents_stream(question):
                    await websocket.send_json(chunk)
                
                print("Streaming complete, connection staying open for next message...")
                continue
                
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                await websocket.send_json({
                    "type": "error",
                    "content": "Invalid message format"
                })
                continue
            
            except RuntimeError as e:
                # Client disconnected during message handling
                if "disconnect" in str(e).lower():
                    print(f"Client disconnected during message handling")
                    break
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
                continue
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    
    except Exception as e:
        print(f"WebSocket fatal error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        manager.disconnect(websocket)
