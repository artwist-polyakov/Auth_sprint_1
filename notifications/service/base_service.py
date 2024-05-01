from abc import ABC

from db.storage.tasks_storage import TasksStorage


class BaseService(ABC):

    def __init__(self, storage: TasksStorage):
        self._storage = storage
