from abc import ABC, abstractmethod


class RateLimitter(ABC):

    @abstractmethod
    def add_request(self, key: str, value: str, timeout: int) -> None:
        pass

    @abstractmethod
    def get_num_requests(self, key: str) -> int:
        pass

    @abstractmethod
    def is_within_limit(self, key: str, max_requests) -> bool:
        pass
