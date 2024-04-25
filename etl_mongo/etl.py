import asyncio  # noqa
import json
import time
from datetime import datetime, timezone
from uuid import UUID

from beanie import WriteRules
from core.settings import get_settings
from db.beanie import BeanieService
from db.kafka_storage import KafkaRepository, get_kafka
from models.bookmark_model import BeanieBookmark
from models.film_model import BeanieFilm
from models.rate_film_model import BeanieRateFilm
from models.rate_review_model import BeanieRateReview
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
                        await in_base.save()

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
                        await in_base.save()

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
                rate = BeanieRateFilm(**data)

                # сначала ищем фильм в базе
                search_criteria = {
                    '_id': data['film_id']
                }

                film_in_base = await BeanieFilm.find(search_criteria).first_or_none()

                if film_in_base is None:
                    # если фильма нет — надо его создать
                    film_in_base = BeanieFilm(
                        id=data['film_id']
                    )
                    await film_in_base.insert()

                # ищем оценку в базе
                search_criteria = {
                    'film._id': data['film_id'],
                    'user_uuid': rate.user_uuid
                }

                rate_in_base = await BeanieRateFilm.find(
                    search_criteria,
                    fetch_links=True
                ).first_or_none()
                print(rate_in_base)
                if rate_in_base is None:
                    film_in_base_cumulative_rating = (
                            film_in_base.rating * film_in_base.likes_counter)
                    film_in_base.likes_counter += 1
                    print(film_in_base_cumulative_rating)
                    film_in_base.rating = (film_in_base_cumulative_rating +
                                           rate.rate) / film_in_base.likes_counter
                    print("обновленный рейтинг фильма")
                    film_in_base_cumulative_rating = ((film_in_base_cumulative_rating + rate.rate)
                                                      / film_in_base.likes_counter)
                    print(film_in_base_cumulative_rating)
                    rate.film = film_in_base
                    await rate.insert(link_rule=WriteRules.WRITE)
                else:
                    rate_in_base.timestamp = rate_in_base.timestamp.replace(tzinfo=timezone.utc)
                    if (rate_in_base.timestamp < rate.timestamp and
                            rate_in_base.film.id == data['film_id'] and
                            rate_in_base.user_uuid == rate.user_uuid):
                        film_in_base_cumulative_rating = (
                                film_in_base.rating * film_in_base.likes_counter)
                        film_in_base_cumulative_rating -= rate_in_base.rate
                        film_in_base_cumulative_rating += rate.rate
                        film_in_base.rating = (
                                film_in_base_cumulative_rating / film_in_base.likes_counter)
                        rate_in_base.film = film_in_base
                        rate_in_base.rate = rate.rate
                        rate_in_base.timestamp = rate.timestamp
                        await rate_in_base.save(link_rule=WriteRules.WRITE)

            case 'rate_review_events':
                rate = BeanieRateReview(**data)

                # сначала ищем отзыв в базе
                search_criteria = {
                    '_id': data['review_id']
                }

                review_in_base = await BeanieReview.find(search_criteria).first_or_none()

                # нельзя оставить оценку несуществущему отзыву
                if review_in_base is not None:

                    # ищем оценку в базе
                    search_criteria = {
                        'review': review_in_base,
                        'user_uuid': rate.user_uuid
                    }

                    rate_in_base = await BeanieRateReview.find(
                        search_criteria,
                        fetch_links=True
                    ).first_or_none()

                    if rate_in_base is None:
                        review_in_base_cumulative_rating = (
                                review_in_base.rating * review_in_base.likes_counter)
                        review_in_base.likes_counter += 1
                        review_in_base.rating = (review_in_base_cumulative_rating +
                                                 rate.rate) / review_in_base.likes_counter
                        await review_in_base.save()
                        rate.review = review_in_base
                        await rate.insert()
                    else:
                        rate_in_base.timestamp = (
                            rate_in_base.timestamp.replace(tzinfo=timezone.utc))
                        if (rate_in_base.timestamp < rate.timestamp and
                                rate_in_base.review.id == data['review_id'] and
                                rate_in_base.user_uuid == rate.user_uuid):
                            review_in_base_cumulative_rating = (review_in_base.rating *
                                                                review_in_base.likes_counter)
                            review_in_base_cumulative_rating -= rate_in_base.rate
                            review_in_base_cumulative_rating += rate.rate
                            review_in_base.rating = (review_in_base_cumulative_rating /
                                                     review_in_base.likes_counter)
                            rate_in_base.rate = rate.rate
                            rate_in_base.timestamp = rate.timestamp
                            rate_in_base.review = review_in_base
                            await rate_in_base.save(link_rule=WriteRules.WRITE)

            case 'delete_film_rate_events':

                search_criteria = {
                    '_id': UUID(data['rate_id'])
                }

                rate_in_base = await BeanieRateFilm.find(
                    search_criteria,
                    fetch_links=True
                ).first_or_none()
                print(rate_in_base)

                if rate_in_base is not None:
                    rate_in_base.timestamp = rate_in_base.timestamp.replace(tzinfo=timezone.utc)
                    film_in_base = rate_in_base.film
                    if (rate_in_base.user_uuid == data['user_uuid'] and
                            rate_in_base.timestamp < datetime.fromtimestamp(
                                data['timestamp'] // 1_000_000_000, timezone.utc)):
                        film_in_base.likes_counter -= 1 if film_in_base.likes_counter > 0 else 0
                        film_in_base.rating = ((film_in_base.rating *
                                                film_in_base.likes_counter -
                                                rate_in_base.rate) /
                                               film_in_base.likes_counter) \
                            if film_in_base.likes_counter else 0
                        rate_in_base.film = film_in_base
                        await rate_in_base.save(link_rule=WriteRules.WRITE)
                        await rate_in_base.delete()
            case 'delete_review_rate_events':
                search_criteria = {
                    '_id': UUID(data['rate_id'])
                }
                rate_in_base = await BeanieRateReview.find(
                    search_criteria,
                    fetch_links=True
                ).first_or_none()
                print(rate_in_base)

                if rate_in_base is not None:
                    rate_in_base.timestamp = rate_in_base.timestamp.replace(tzinfo=timezone.utc)
                    if (rate_in_base.user_uuid == data['user_uuid'] and
                            rate_in_base.timestamp < datetime.fromtimestamp(
                                data['timestamp'] // 1_000_000_000, timezone.utc)):
                        rate_in_base.review.likes_counter -= 1 \
                            if rate_in_base.review.likes_counter > 0 else 0
                        rate_in_base.review.rating = ((rate_in_base.review.rating *
                                                       rate_in_base.review.likes_counter -
                                                       rate_in_base.rate) /
                                                      rate_in_base.review.likes_counter) \
                            if rate_in_base.review.likes_counter else 0
                        await rate_in_base.review.save()
                        await rate_in_base.delete()
            case _:
                print('Unknown type')

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
