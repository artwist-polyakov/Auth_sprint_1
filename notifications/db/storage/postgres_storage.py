import logging
from functools import wraps

from configs.settings import get_postgres_dsn
from db.models.tasks import Tasks
from contextlib import asynccontextmanager
from db.models.notifications import Notifications
from db.requests.task_request import PostTask
from db.responses.task_response import TaskResponse
from db.storage.tasks_storage import TasksStorage
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.sql import func


class PostgresStorage(TasksStorage):

    def __init__(self):
        self._dsn = get_postgres_dsn()
        self._engine = create_async_engine(self._dsn, echo=True, future=True)
        self._async_session = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def session_manager(self):
        async with self._async_session() as session:
            try:
                yield session
            except Exception as e:
                print(e)
                await session.rollback()
            finally:
                await session.close()

    @staticmethod
    def _with_session(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            instance = args[0]  # получаем self из метода
            async with instance.session_manager() as session:
                return await func(*args, session=session, **kwargs)

        return wrapper

    async def get_task(self, task_id: int, session=None) -> TaskResponse | None:
        task = await self._get_task_info(task_id)
        if task is None:
            return None
        statistics = await self._get_task_statistics(task_id)
        return TaskResponse(
            id=task.id,
            title=task.title,
            sended_messages=statistics,
            total_messages=len(task.user_ids),
            type=task.type,
            created_at=int(task.created_at.timestamp()),
            is_launched=task.is_launched
        )

    @_with_session
    async def _get_task_info(self, task_id: int, session=None) -> Tasks | None:
        try:
            query = select(Tasks).where(Tasks.id == task_id)
            result = await session.execute(query)
            task = result.scalar_one_or_none()
            return task
        except Exception as e:
            print(e)
            return None

    @_with_session
    async def _get_task_statistics(self, task_id: int, session=None) -> int:
        try:
            query = select(
                func.count()
            ).where(Notifications.task_id == task_id and Notifications.is_sended)
            result = await session.execute(query)
            return result.scalar()
        except Exception as e:
            print(e)
            return 0

    @_with_session
    async def create_task(self, task: PostTask, session=None) -> TaskResponse | None:
        try:
            async with session.begin():
                task__to_save = Tasks(
                    title=task.title,
                    content=task.content,
                    user_ids=task.user_ids,
                    type=task.type
                )
                session.add(task__to_save)
                await session.commit()
                return TaskResponse(
                    id=task__to_save.id,
                    title=task__to_save.title,
                    sended_messages=0,
                    total_messages=len(task__to_save.user_ids),
                    type=task__to_save.type,
                    created_at=int(task__to_save.created_at.timestamp()),
                    is_launched=task__to_save.is_launched
                )
        except Exception as e:
            logging.error(e)
            return None

    def close(self):
        self._engine.dispose()
