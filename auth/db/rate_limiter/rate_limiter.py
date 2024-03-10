from abc import ABC, abstractmethod


class RateLimitter(ABC):

    @abstractmethod
    async def add_request(self, key: str, value: str, timeout: int) -> None:
        pass

    @abstractmethod
    async def get_num_requests(self, key: str) -> int:
        pass

    @abstractmethod
    async def is_within_limit(self, key: str, max_requests) -> bool:
        pass
