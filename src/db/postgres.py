from configs.settings import PostgresSettings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from db.auth.user import Base
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

    async def create_database(self, model: Base) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(model.metadata.create_all)

    async def add_data(self, request: Base) -> str:
        # INSERT запрос
        async with self._async_session() as session:
            try:
                session.add(request)
                await session.commit()
            except Exception as e:
                await session.rollback()
                error_type = type(e).__name__
                return error_type
            else:
                return 'Success'

    # async def get_data(self, model: Base):
    #     # SELECT запрос
    #     async with self.get_session() as session:
    #         result = await session.execute(select(model))
    #         data = result.scalars().all()
    #         return data

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
