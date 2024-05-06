from abc import ABC, abstractmethod


class TasksStorage(ABC):

    @abstractmethod
    def edit_notification_error_true(self, task_id: int):
        pass

    @abstractmethod
    def edit_notification_sent_true(self, notification_id: int):
        pass

    @abstractmethod
    def close(self):
        pass
