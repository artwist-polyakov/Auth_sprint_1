from abc import ABC, abstractmethod

from db.requests.task_request import PostTask
from db.responses.task_response import TaskResponse


class TasksStorage(ABC):

    @abstractmethod
    async def create_task(self, task: PostTask) -> TaskResponse | None:
        pass

    @abstractmethod
    async def get_task(self, task_id: int) -> TaskResponse | None:
        pass
