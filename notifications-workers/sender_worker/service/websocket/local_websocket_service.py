import os

import websockets
from configs.settings import get_settings
from service.websocket.websocket_service import WebsocketService


class LocalWebsocketService(WebsocketService):

    def __init__(self):
        self.name = os.getenv("WORKER_ID", "worker_unknown")
        websocket_settings = get_settings().get_websocket_settings()
        self._uri = f"ws://{websocket_settings.host}:{websocket_settings.port}"
        self._websocket = None

    async def connect(self):
        self._websocket = await websockets.connect(self._uri)
        await self._websocket.send(self.name)

    async def send_message(self, user_id: str, message: str) -> bool:
        if not self._websocket:
            return False
        try:
            await self._websocket.send(f"{user_id}: {message}")
            response = await self._websocket.recv()
            return response == "ОК"
        except websockets.exceptions.ConnectionClosed:
            return False

    async def close(self):
        if self._websocket:
            await self._websocket.close()
