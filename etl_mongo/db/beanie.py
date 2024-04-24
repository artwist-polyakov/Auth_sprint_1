from beanie import init_beanie
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from datetime import datetime, timezone
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import Field


class BeanieBookmark(Document):
    id: UUID = Field(default_factory=uuid4)
    user_uuid: Indexed(str)
    film_id: Indexed(str)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "bookmarks"


class BeanieService:

    def __init__(self):
        self._connection_string = 'mongodb://mongo1:27017,node2:27017,node3:27017/?replicaSet=myReplicaSet'
        self._database = 'movies_content'
        self.client = None

    async def init(self):
        self.client = AsyncIOMotorClient(self._connection_string)
        await init_beanie(self.client[self._database], document_models=[BeanieBookmark])
        print('Beanie has been initialized')

    async def close(self):
        await self.client.close()
        print('Beanie has been closed')
