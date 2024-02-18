import logging

from fastapi import Response, status
from sqlalchemy import text, select
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from configs.settings import PostgresSettings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from db.auth.user import Base, User
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

    async def add_data(self, request: Base) -> Response:
        # INSERT запрос
        async with self._async_session() as session:
            try:
                session.add(request)
                await session.commit()
                return Response(content='', status_code=status.HTTP_201_CREATED)

            except SQLAlchemyError as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return Response(content='', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return Response(content='', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def get_single_data(self, field_name: str, field_value) -> User | None:
        # SELECT запрос
        async with self._async_session() as session:
            try:
                if field_name == 'uuid':
                    query = select(User).where(User.uuid == field_value)
                elif field_name == 'login':
                    query = select(User).where(User.login == field_value)

                query_result = await session.execute(query)
                user = query_result.scalar_one_or_none()
                if not user:
                    return None
                return user

            except NoResultFound as e:
                logging.error(type(e).__name__, e)
                return None

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return None

    async def delete_single_data(self, uuid) -> Response:
        # DELETE запрос
        async with self._async_session() as session:
            try:
                record = await self.get_single_data(
                    field_name='uuid',
                    field_value=uuid
                )
                if not record:
                    return Response(content='', status_code=status.HTTP_404_NOT_FOUND)
                await session.delete(record)
                await session.commit()
                return Response(content='', status_code=status.HTTP_200_OK)

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return Response(content='',
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # async def get_all_data(self, model: Base):
    #     # SELECT запрос
    #     pass

    # async def update_data(self, model: Base):
    #     # UPDATE запрос
    #     async with await self.get_session() as session:
    #         result = await session.execute(select(model).where(model.id == 1))
    #         record = result.scalars().one_or_none()
    #         if record:
    #             record.value = 456
    #             await session.commit()
