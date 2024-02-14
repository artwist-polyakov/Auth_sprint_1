from configs.settings import PostgresSettings
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Создаём базовый класс для будущих моделей
Base = declarative_base()

pstg = PostgresSettings()
dsn = f'postgresql+asyncpg://{pstg.user}:{pstg.password}@{pstg.host}:{pstg.port}/{pstg.db}'
# Укажите echo=True – так вы сможете увидеть сгенерированные SQL-запросы в консоли
engine = create_async_engine(dsn, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def create_database(model=Base) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(model.metadata.create_all)


async def purge_database(model=Base) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(model.metadata.drop_all)

