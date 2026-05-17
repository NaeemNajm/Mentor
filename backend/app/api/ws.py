from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()

@router.websocket("/updates")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for broadcasting realtime updates.
    Final route will be /api/ws/updates because the router is included with prefix "/api/ws" in main.py.
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo/broadcast received payload to all listeners
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
