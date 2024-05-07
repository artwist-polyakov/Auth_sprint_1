from abc import ABC, abstractmethod


class WebsocketService(ABC):

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def send_message(self, user_id: str, message: str) -> bool:
        pass

    @abstractmethod
    async def close(self):
        pass
