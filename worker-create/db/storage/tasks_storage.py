from abc import ABC, abstractmethod

from models.single_task import SingleTask


class TasksStorage(ABC):

    @abstractmethod
    def save_notification(self, task: SingleTask) -> SingleTask:
        pass

    @abstractmethod
    def close(self):
        pass
