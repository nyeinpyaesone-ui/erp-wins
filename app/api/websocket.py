"""
ERP Platform — WebSocket Endpoint

WebSocket is notification transport only.
PostgreSQL remains authoritative.
Clients must recover current state after reconnect.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["websocket"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    WebSocket endpoint for real-time notifications.
    
    Rules:
    - WebSocket is not authoritative state
    - Events must not depend on successful WebSocket delivery
    - Clients must recover state after reconnect
    """
    await websocket.accept()
    
    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            
            # Echo back for now (placeholder)
            await websocket.send_text(f"Message received: {data}")
            
    except WebSocketDisconnect:
        # Client disconnected — this is expected
        pass
