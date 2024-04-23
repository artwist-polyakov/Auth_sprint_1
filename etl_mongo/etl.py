import asyncio  # noqa
import json
import time

from core.settings import get_settings
from db.kafka_storage import KafkaRepository, get_kafka
from db.mongo import MongoService
from models.bookmark_model import MongoBookmark


class ETL:
    _kafka_bootstrap_servers = [f'{get_settings().kafka.host}:{get_settings().kafka.port}']
    _mongo = MongoService()

    def __init__(self):
        self._topics = ['player_events', 'view_events', 'custom_events']

    def get_mongo(self):
        return self._mongo

    async def load(self, storage: MongoService, data, type):
        match (type):
            case 'delete_bookmark_events':
                pass
                # storage.delete(data["film_id"])
            case 'add_bookmark_events':
                print(data)
                t = MongoBookmark(
                    user_uuid=data['user_uuid'],
                    film_uuid=data['film_id'],
                )
                storage.data_recording(
                    data=[t.model_dump()],
                    collection_name='bookmarks')

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

    async def run(self, mongo: MongoService):
        consumer = await get_kafka().consume()
        try:
            for msg in consumer:
                data = json.loads(msg.value.decode('utf-8'))
                topic = msg.topic
                if data is not None:
                    await self.load(mongo, data, topic)
                    await KafkaRepository.commit(consumer, msg)
        finally:
            consumer.close()


if __name__ == "__main__":
    print('ETL started')
    etl = ETL()
    with etl.get_mongo() as mongo_db:
        while True:
            print("Conected to mongo")
            asyncio.run(etl.run(mongo_db))
            print('ETL finished')
            time.sleep(20)
