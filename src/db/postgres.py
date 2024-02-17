import logging

from sqlalchemy import text, select
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from configs.settings import PostgresSettings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from db.auth.user import Base
from db.auth.user_storage import UserStorage
from db.models.auth_responses.user_response import UserResponse


class PostgresProvider(UserStorage):
    def __init__(self):
        self._pstg = PostgresSettings()
        self._dsn = (f'postgresql+asyncpg://'
                     f'{self._pstg.user}:{self._pstg.password}@{self._pstg.host}:'
                     f'{self._pstg.port}/{self._pstg.db}')
        self._engine = create_async_engine(self._dsn, echo=True, future=True)
        self._async_session = sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def create_schema(self, schema_name: str) -> None:
        async with self._engine.begin() as conn:
            await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};"))

    async def create_database(self, model: Base) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(model.metadata.create_all)

    async def add_data(self, request: Base) -> str:
        """
        Выполняет INSERT запрос
        :param request: объект-request, который наследуется от Base
        :return: ответ
        """
        # INSERT запрос
        async with self._async_session() as session:
            try:
                session.add(request)
                await session.commit()
                return '201_success'

            except SQLAlchemyError as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return '500_sqlalchemy_error'

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return '500_unknown_error'

    async def get_single_data(self, **params) -> UserResponse | None:
        """
        Выполняет SELECT запрос для поиска одной записи
        :param params: словарь {"имя параметра":"значение параметра"},
        по которым происходит поиск
        :return: объект UserResult или None, если запись не найдена
        """
        async with self._async_session() as session:
            try:
                query = select(UserResponse).filter_by(**params)
                result = await session.execute(query)
                return result.scalar_one()

            except NoResultFound as e:
                logging.error(type(e).__name__, e)
                return None

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return None

    async def get_multiple_data(self, model: Base):
        # SELECT запрос (несколько записей)
        pass

    # async def update_data(self, model: Base):
    #     # UPDATE запрос
    #     async with await self.get_session() as session:
    #         result = await session.execute(select(model).where(model.id == 1))
    #         record = result.scalars().one_or_none()
    #         if record:
    #             record.value = 456
    #             await session.commit()
    #
    # async def delete_data(self, model: Base):
    #     # DELETE запрос
    #     async with await self.get_session() as session:
    #         result = await session.execute(select(model).where(model.id == 1))
    #         record = result.scalars().one_or_none()
    #         if record:
    #             await session.delete(record)
    #             await session.commit()
