import logging
from contextlib import contextmanager
from functools import wraps

from configs.settings import get_postgres_dsn
from db.models.notifications import Notifications  # noqa
from db.models.tasks import Tasks
from db.storage.tasks_storage import TasksStorage
from models.task_result import TaskResult
from sqlalchemy import create_engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker


class PostgresStorage(TasksStorage):

    def __init__(self):
        self._dsn = get_postgres_dsn()
        logging.error(self._dsn)
        print(self._dsn)
        self._engine = create_engine(self._dsn)
        self._session = sessionmaker(bind=self._engine)

    @contextmanager
    def session_manager(self) -> Session:
        """ Контекстный менеджер для управления сессиями SQLAlchemy. """
        session = self._session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"An error occurred: {e}")
            raise
        finally:
            session.close()

    def _with_session(func):
        """ Декоратор для методов, которым нужна сессия. """

        @wraps(func)
        def wrapper(self, *args, **kwargs):  # добавляем self здесь
            with self.session_manager() as session:
                return func(self, *args, session=session, **kwargs)  # передаем self далее в func

        return wrapper

    @_with_session
    def getNewTasks(self, session=None) -> list[TaskResult]:
        tasks = session.execute(select(Tasks).where(Tasks.is_launched.is_(False)))
        result = []
        for task in tasks.scalars().all():
            result.append(
                TaskResult(
                    id=task.id,
                    title=task.title,
                    content=task.content,
                    user_ids=task.user_ids,
                    type=task.type,
                    created_at=int(task.created_at.timestamp()),
                    is_launched=task.is_launched)
            )
        return result

    @_with_session
    def markTaskLaunched(self, task_id: int, session=None) -> bool:
        task = select(Tasks).where(Tasks.id == task_id)
        task = session.execute(task).first()
        if task is None:
            return False
        task.is_launched = True
        return True

    def close(self):
        self._engine.dispose()
