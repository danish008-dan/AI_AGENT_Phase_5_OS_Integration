# File: os_layer/websocket/log_stream.py

from fastapi import WebSocket

# ==============================
# Active WebSocket Connections
# ==============================
active_connections = []


# ==============================
# Connect WebSocket
# ==============================
async def connect(websocket: WebSocket):
    """
    Accepts a new WebSocket connection and adds it to active connections.
    """
    await websocket.accept()
    active_connections.append(websocket)


# ==============================
# Broadcast Message
# ==============================
async def broadcast(message: str):
    """
    Sends a message to all active WebSocket connections.
    """
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception:
            # Remove disconnected clients
            active_connections.remove(connection)