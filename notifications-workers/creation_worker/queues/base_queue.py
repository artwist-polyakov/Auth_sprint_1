from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar

T = TypeVar('T')


class BaseQueue(ABC):

    @abstractmethod
    def push(self, message: T) -> bool:
        pass

    @abstractmethod
    def pop(self, handler: Callable[[Any, Any, Any, bytes], None]):
        pass

    @abstractmethod
    def close(self):
        pass
