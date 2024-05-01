import logging
from functools import lru_cache

from db.requests.base_request import BaseRequest
from db.requests.task_request import PostTask, GetTaskInfo, TaskRequest
from fastapi import Depends
from db.responses.task_response import TaskResponse
from db.storage.postgres_storage import PostgresStorage
from db.storage.tasks_storage import TasksStorage
from service.base_service import BaseService


class TasksService(BaseService):

    async def handle_task_request(self, request: BaseRequest) -> TaskResponse | None:
        match request:
            case TaskRequest():
                return await self._storage.create_task(PostTask(**request.model_dump()))
            case GetTaskInfo():
                return await self._storage.get_task(request.task_id)
            case _:
                return None


@lru_cache()
def get_tasks_service(
        storage: TasksStorage = Depends(PostgresStorage)
) -> TasksService:
    return TasksService(storage)
