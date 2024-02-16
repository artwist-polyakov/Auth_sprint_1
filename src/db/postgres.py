from sqlalchemy import select
from sqlalchemy.exc import OperationalError, IntegrityError

from configs.settings import PostgresSettings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from db.auth.user import Base


class PostgresProvider:
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

    # async def get_session(self) -> AsyncSession:
    #     async with self._async_session() as session:
    #         yield session

    async def get_session(self) -> AsyncSession:
        return self._async_session()
    # todo закрыть соединение

    async def create_database(self, model: Base) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(model.metadata.create_all)

    async def purge_database(self, model: Base) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(model.metadata.drop_all)

    # async def get_data(self, model: Base):
    #     # SELECT запрос
    #     async with self.get_session() as session:
    #         result = await session.execute(select(model))
    #         data = result.scalars().all()
    #         return data

    async def add_data(self, request: Base):
        try:
            async with await self.get_session() as session:
                session.add(request)
                await session.commit()
            return True
        except OperationalError as e:
            return False
        except IntegrityError as e:
            return False
        # SQLAlchemyError - все возможные ошибки

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
