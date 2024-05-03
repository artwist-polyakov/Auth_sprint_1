from abc import ABC, abstractmethod

from models.task_result import TaskResult


class BaseQueue(ABC):

    @abstractmethod
    def push(self, task: TaskResult) -> bool:
        pass

    @abstractmethod
    def pop(self) -> dict:
        pass

    @abstractmethod
    def close(self):
        pass
