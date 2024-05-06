from configs.settings import get_settings
from db.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class PostgresClient:
    def __init__(self):
        self._dsn = get_settings().get_auth_postgres_dsn()
        self._engine = create_async_engine(self._dsn, echo=True, future=True)
        self._async_session = sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_user(self, user_id):
        async with self._async_session() as session:
            try:
                query = select(User).where(User.uuid == user_id)

                query_result = await session.execute(query)
                user = query_result.scalar_one_or_none()
                if not user:
                    return None
                return user
            except Exception as e:
                await session.rollback()
                return {'error': f"{e}", 'content': 'error'}
