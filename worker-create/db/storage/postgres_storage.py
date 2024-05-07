import logging
from contextlib import contextmanager
from functools import wraps

from configs.settings import get_settings
from db.models.notifications import Notifications  # noqa
from db.models.tasks import Tasks
from db.storage.tasks_storage import TasksStorage
from models.single_task import SingleTask
from sqlalchemy import create_engine, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker


class PostgresStorage(TasksStorage):

    def __init__(self):
        self._dsn = get_settings().get_postgres_dsn()
        self._engine = create_engine(self._dsn)
        self._session = sessionmaker(bind=self._engine)
        logging.warning(f"PostgresStorage initialized with DSN: {self._dsn}")

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
    def save_notification(self, task: SingleTask, session=None) -> SingleTask:
        query = select(Tasks).where(Tasks.id == task.task_id)
        task_from_base = session.execute(query).scalar()
        notification = Notifications(
            task_id=task.task_id,
            user_id=task.user_id,
            is_sended=False,
            is_error=False,
            task=task_from_base
        )
        session.add(notification)
        session.commit()
        task.id = notification.id
        return task

    def close(self):
        self._engine.dispose()
