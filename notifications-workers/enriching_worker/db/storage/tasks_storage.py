from abc import ABC, abstractmethod


class TasksStorage(ABC):

    @abstractmethod
    def mark_as_error(self, notification: int) -> bool:
        pass

    @abstractmethod
    def close(self):
        pass
