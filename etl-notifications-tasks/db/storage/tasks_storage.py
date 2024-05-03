from abc import ABC, abstractmethod
from models.task_result import TaskResult


class TasksStorage(ABC):

    @abstractmethod
    def getNewTasks(self) -> list[TaskResult]:
        pass

    @abstractmethod
    def markTaskLaunched(self, task_id: int) -> bool:
        pass

    @abstractmethod
    def close(self):
        pass
