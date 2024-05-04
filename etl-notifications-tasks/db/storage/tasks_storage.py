from abc import ABC, abstractmethod

from models.task_result import TaskResult


class TasksStorage(ABC):

    @abstractmethod
    def get_new_tasks(self) -> list[TaskResult]:
        pass

    @abstractmethod
    def mark_task_as_launched(self, task_id: int) -> bool:
        pass

    @abstractmethod
    def close(self):
        pass
