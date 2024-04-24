from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.bookmark_model import BeanieBookmark


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
