import asyncio  # noqa
import json
import time
from datetime import datetime, timezone

from core.settings import get_settings
from db.beanie import BeanieService
from db.kafka_storage import KafkaRepository, get_kafka
from models.bookmark_model import BeanieBookmark
from models.review_model import BeanieReview


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
                bookmark = BeanieBookmark(**data)

                search_criteria = {
                    'film_id': bookmark.film_id,
                    'user_uuid': bookmark.user_uuid
                }

                # получаем все закладки с таким же film_id
                in_base = await BeanieBookmark.find(search_criteria).to_list()

                if in_base:
                    print(in_base)
                    # удаляем закладку если пользователь запроса совпадает по id пользователя базы
                    for bookmark in in_base:
                        if (  # проверка, что запрос удаления моложе последней записи
                                bookmark.user_uuid == data['user_uuid'] and
                                bookmark.timestamp.replace(
                                    tzinfo=timezone.utc
                                ) <= datetime.fromtimestamp(
                                data['timestamp'] // 1_000_000_000, timezone.utc
                                )
                        ):
                            await bookmark.delete()

            case 'add_bookmark_events':
                bookmark = BeanieBookmark(**data)

                search_criteria = {
                    'film_id': bookmark.film_id,
                    'user_uuid': bookmark.user_uuid
                }

                # получаем все закладки с таким же film_id
                in_base = await BeanieBookmark.find(search_criteria).first_or_none()
                print(in_base)

                if in_base is None:
                    # если закладки с таким film_id нет, то добавляем новую
                    await bookmark.insert()
                else:
                    in_base.timestamp = in_base.timestamp.replace(tzinfo=timezone.utc)
                    # только если у закладки время создания меньше,
                    # то обновляем закладку в базе
                    if in_base is not None and in_base.timestamp < bookmark.timestamp:
                        in_base.created_at = bookmark.created_at
                        await in_base.update()

            case 'review_events':
                review = BeanieReview(**data)

                search_criteria = {
                    '_id': review.id
                }

                in_base = await BeanieReview.find(search_criteria).first_or_none()
                print(in_base)

                if in_base is None:
                    await review.insert()
                else:
                    in_base.timestamp = in_base.timestamp.replace(tzinfo=timezone.utc)
                    if (in_base is not None
                            and in_base.timestamp < review.timestamp
                            and in_base.film_id == review.film_id
                            and in_base.user_uuid == review.user_uuid):
                        in_base.content = review.content
                        in_base.timestamp = review.timestamp
                        await in_base.update()

            case 'delete_review_events':
                review = BeanieReview(**data)

                search_criteria = {
                    '_id': review.id
                }

                in_base = await BeanieReview.find(search_criteria).first_or_none()
                print(in_base)

                if in_base is not None:
                    in_base.timestamp = in_base.timestamp.replace(tzinfo=timezone.utc)
                    if (
                            in_base.user_uuid == review.user_uuid
                            and in_base.timestamp < review.timestamp):
                        await in_base.delete()

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
