from abc import ABC, abstractmethod


class CacheStorage(ABC):
    @abstractmethod
    async def get_cache(self, key: str) -> str:
        pass

    @abstractmethod
    async def put_cache(self, key: str, value: str, expired=0) -> None:
        pass

    @abstractmethod
    async def close(self):
        pass
