import logging

from pydantic import BaseModel
from sqlalchemy import insert, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from configs.settings import PostgresSettings
from db.auth.refresh_token import RefreshToken
from db.auth.role import Role
from db.auth.user import Base, User
from db.auth.user_storage import UserStorage


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

    async def add_single_data(self, request: BaseModel, entity: str) -> dict:
        # INSERT запрос
        async with self._async_session() as session:
            try:
                match entity:
                    case 'user':
                        query = (
                            insert(User)
                            .values(
                                uuid=request.uuid,
                                login=request.login,
                                password=request.password,
                                first_name=request.first_name,
                                last_name=request.last_name
                            )
                        )
                    case 'refresh_token':
                        query = (
                            insert(RefreshToken)
                            .values(
                                uuid=request.refresh_id,
                                user_id=request.user_id,
                                active_till=request.active_till
                            )
                        )
                    case 'role':
                        query = (
                            insert(Role)
                            .values(
                                role=request.role,
                                resource=request.resource,
                                verb=request.verb
                            )
                        )
                await session.execute(query)
                await session.commit()
                return {'status_code': 201, 'content': f'{entity} created'}

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return {'status_code': 500, 'content': 'error'}

    async def get_single_user(
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

    async def delete_single_data(self, uuid: str, entity: str) -> dict:
        # DELETE запрос
        async with self._async_session() as session:
            try:
                match entity:
                    case 'user':
                        result: User | dict = await self.get_single_user(
                            field_name='uuid',
                            field_value=uuid
                        )
                    case 'role':
                        result: Role | dict = await self.get_single_role(uuid)

                if isinstance(result, dict):
                    return result
                await session.delete(result)
                await session.commit()
                return {'status_code': 200, 'content': 'success'}

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return {'status_code': 500, 'content': 'error'}

    async def update_single_user(self, request: BaseModel) -> dict:
        # UPDATE запрос
        async with self._async_session() as session:
            try:
                query = (
                    update(User)
                    .where(User.uuid == request.uuid)
                    .values(
                        login=request.login,
                        first_name=request.first_name,
                        last_name=request.last_name
                    )
                )
                await session.execute(query)
                await session.commit()
                return {'status_code': 200, 'content': 'success'}

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return {'status_code': 500, 'content': 'error'}

    async def get_refresh_token(self, refresh_token: str):
        # SELECT запрос
        async with self._async_session() as session:
            try:
                query = select(RefreshToken).where(RefreshToken.refresh_id == refresh_token)
                result = await session.execute(query)
                return result.scalar_one_or_none()

            except Exception as e:
                logging.error(type(e).__name__, e)
                return None

    async def update_refresh_token(
            self,
            new_refresh_token: RefreshToken,
            old_refresh_token_id: str
    ):
        # todo обозначить типы возвращаемых значений
        async with self._async_session() as session:
            try:
                query = (
                    update(
                        RefreshToken
                    )
                    .where(
                        RefreshToken.refresh_id == old_refresh_token_id
                    )
                    .values(
                        active_till=new_refresh_token.active_till,
                        refresh_id=new_refresh_token.refresh_id
                    )
                )
                await session.execute(query)
                await session.commit()
                return True

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return False

    async def get_roles(self) -> dict:
        # SELECT запрос
        async with self._async_session() as session:
            try:
                query = select(Role)
                roles = await session.execute(query)
                await session.commit()

                # todo converter
                roles_result = dict()

                roles = roles.all()
                for role_instance in roles:
                    role_instance = role_instance[0].__dict__
                    role_name = role_instance['role']
                    resource = role_instance['resource']
                    verb = role_instance['verb']

                    if role_name in roles_result:
                        if resource in roles_result[role_name]:
                            roles_result[role_name][resource].append(verb)
                        else:
                            roles_result[role_name][resource] = [verb]
                    else:
                        roles_result[role_name] = {resource: [verb]}

                return roles_result

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return {}

    async def get_single_role(self, uuid: str) -> Role | dict:
        # SELECT запрос
        async with self._async_session() as session:
            try:
                query = select(Role).where(Role.uuid == uuid)
                query_result = await session.execute(query)
                role = query_result.scalar_one_or_none()
                if not role:
                    return {'status_code': 404, 'content': 'role not found'}
                return role

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return {'status_code': 500, 'content': 'error'}

    async def update_role(self, request: BaseModel) -> dict:
        # UPDATE запрос
        async with self._async_session() as session:
            try:
                query = (
                    update(Role)
                    .where(Role.uuid == request.uuid)
                    .values(
                        role=request.role,
                        resource=request.resource,
                        verb=request.verb
                    )
                )
                await session.execute(query)
                await session.commit()
                return {'status_code': 200, 'content': 'success'}

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return {'status_code': 500, 'content': 'error'}

    async def update_user_role(self, uuid: str, new_role: str) -> dict:
        # UPDATE запрос
        async with self._async_session() as session:
            try:
                query = (
                    update(User)
                    .where(User.uuid == uuid)
                    .values(
                        role=new_role
                    )
                )
                await session.execute(query)
                await session.commit()
                return {'status_code': 200, 'content': 'success'}

            except Exception as e:
                await session.rollback()
                logging.error(type(e).__name__, e)
                return {'status_code': 500, 'content': 'error'}
