from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.settings import pstg_dsn


class PostgresClient:
    def __init__(self):
        self._dsn = pstg_dsn
        self._engine = create_async_engine(self._dsn, echo=True, future=True)
        self._async_session = sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_films(self):
        async with self._async_session() as session:
            query = await session.execute(text("SELECT id FROM content.film_work LIMIT 500"))
            films = [uuid for (uuid,) in query]
            return films
