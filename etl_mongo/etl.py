import asyncio  # noqa
import json
import time

from core.settings import get_settings
from db.kafka_storage import KafkaRepository, get_kafka
from db.mongo import MongoService
from db.beanie import BeanieService, BeanieBookmark
from models.bookmark_model import MongoBookmark


class ETL:
    _kafka_bootstrap_servers = [f'{get_settings().kafka.host}:{get_settings().kafka.port}']

    def __init__(self):
        self._topics = ['player_events', 'view_events', 'custom_events']
        self._beanie_service = BeanieService()

    async def init_services(self):
        await self._beanie_service.init()

    async def close_services(self):
        await self._beanie_service.close()

    async def load(self, data, type):
        print(type)
        print(data)
        match (type):
            case 'delete_bookmark_events':
                pass
                # storage.delete(data["film_id"])
            case 'add_bookmark_events':
                bookmark = BeanieBookmark(**data)
                await bookmark.insert()

            case 'review_events':
                print(data)
            case 'delete_review_events':
                print(data)
            case 'rate_movie_events':
                print(data)
            case 'rate_review_events':
                print(data)
            case 'delete_rate_events':
                print(data)

    async def run(self):
        consumer = await get_kafka().consume()
        try:
            for msg in consumer:
                data = json.loads(msg.value.decode('utf-8'))
                topic = msg.topic
                if data is not None:
                    await self.load(data, topic)
                    await KafkaRepository.commit(consumer, msg)
        finally:
            consumer.close()


async def main():
    print('ETL started')
    etl = ETL()
    await etl.init_services()

    while True:
        print("Connected to mongo")
        await etl.run()
        print('ETL finished')
        await asyncio.sleep(20)


if __name__ == "__main__":
    time.sleep(5)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
