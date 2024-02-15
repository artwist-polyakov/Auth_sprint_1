from sqlalchemy import select

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

    async def get_session(self) -> AsyncSession:
        async with self._async_session() as session:
            yield session

    async def create_database(self, model: Base) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(model.metadata.create_all)

    async def purge_database(self, model: Base) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(model.metadata.drop_all)

    async def get_data(self, model: Base):
        async with self.get_session() as session:
            # SELECT запрос
            result = await session.execute(select(model))
            data = result.scalars().all()
            return data

    async def add_data(self, model: Base):
        async with self.get_session() as session:
            # INSERT запрос
            new_record = model(name='Test', value=123)
            session.add(new_record)
            await session.commit()

    async def update_data(self, model: Base):
        async with self.get_session() as session:
            # UPDATE запрос
            result = await session.execute(select(model).where(model.id == 1))
            record = result.scalars().one_or_none()
            if record:
                record.value = 456
                await session.commit()

    async def delete_data(self, model: Base):
        async with self.get_session() as session:
            # DELETE запрос
            result = await session.execute(select(model).where(model.id == 1))
            record = result.scalars().one_or_none()
            if record:
                await session.delete(record)
                await session.commit()
