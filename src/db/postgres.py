import logging

from fastapi import Response
from sqlalchemy import text, select

from configs.settings import PostgresSettings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from db.auth.user import Base, User
from db.auth.user_storage import UserStorage


# todo вынести "except Exception as e" из всех методов

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
                # todo return uuid (по REST)
                return Response(status_code=201)

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return Response(status_code=500)

    async def get_single_data(
            self,
            field_name: str,
            field_value
    ) -> User | Response:
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
                    return Response(status_code=404)
                return user

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return Response(status_code=500)

    async def delete_single_data(self, uuid) -> Response:
        # DELETE запрос
        async with self._async_session() as session:
            try:
                result: User | Response = await self.get_single_data(
                    field_name='uuid',
                    field_value=uuid
                )
                if isinstance(result, Response):
                    return result
                await session.delete(result)
                await session.commit()
                return Response(status_code=200)

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return Response(status_code=500)

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
