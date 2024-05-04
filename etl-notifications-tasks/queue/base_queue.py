from abc import ABC, abstractmethod
from typing import Any, Callable

from models.task_result import TaskResult


class BaseQueue(ABC):

    @abstractmethod
    def push(self, task: TaskResult) -> bool:
        pass

    @abstractmethod
    def pop(self, handler: Callable[[Any, Any, Any, bytes], None]):
        pass

    @abstractmethod
    def close(self):
        pass
