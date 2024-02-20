import logging

from pydantic import BaseModel
from sqlalchemy import select, text, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from configs.settings import PostgresSettings
from db.auth.user import Base, User
from db.auth.user_storage import UserStorage
from db.models.auth_db_requests.user_request import UserRequest
from db.models.auth_db_requests.user_update_request import UserUpdateRequest


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

    async def add_single_data(self, request: BaseModel) -> dict:
        # INSERT запрос
        async with self._async_session() as session:
            try:
                db_request = UserRequest(
                    uuid=request.uuid,
                    login=request.login,
                    password=request.password,
                    first_name=request.first_name,
                    last_name=request.last_name,
                    is_verified=request.is_verified
                )
                session.add(db_request)
                await session.commit()
                return {'status_code': 201, 'content': 'user created'}

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return {'status_code': 500, 'content': 'error'}

    async def get_single_data(
            self,
            field_name: str,
            field_value
    ) -> User | dict:
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
                    return {'status_code': 404, 'content': 'user not found'}
                return user

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return {'status_code': 500, 'content': 'error'}

    async def delete_single_data(self, uuid) -> dict:
        # DELETE запрос
        async with self._async_session() as session:
            try:
                result: User | dict = await self.get_single_data(
                    field_name='uuid',
                    field_value=uuid
                )
                if isinstance(result, dict):
                    return result
                await session.delete(result)
                await session.commit()
                return {'status_code': 200, 'content': 'success'}

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return {'status_code': 500, 'content': 'error'}

    async def update_single_data(self, request: BaseModel) -> dict:
        # UPDATE запрос
        async with self._async_session() as session:
            try:
                # todo м.б. можно лучше
                db_request = UserUpdateRequest(
                    uuid=request.uuid,
                    login=request.login,
                    first_name=request.first_name,
                    last_name=request.last_name
                )
                query = (
                    update(User)
                    .where(User.uuid == db_request.uuid)
                    .values(
                        login=db_request.login,
                        first_name=db_request.first_name,
                        last_name=db_request.last_name
                    )
                )
                await session.execute(query)
                await session.commit()
                return {'status_code': 200, 'content': 'success'}

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return {'status_code': 500, 'content': 'error'}
