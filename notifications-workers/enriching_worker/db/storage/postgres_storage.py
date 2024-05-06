import logging
from contextlib import contextmanager
from functools import wraps

from configs.settings import get_settings
from db.models.notifications import Notifications  # noqa
from db.models.tasks import Tasks  # noqa
from db.storage.tasks_storage import TasksStorage
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
    def mark_as_error(self, notification: int, session=None) -> bool:
        query = select(Notifications).where(Notifications.id == notification)
        notification_obj = session.execute(query).scalar()
        if notification_obj:
            notification_obj.is_error = True
        else:
            logging.error("Notification not found")

    def close(self):
        self._engine.dispose()
