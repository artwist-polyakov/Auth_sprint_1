import asyncio
import logging
import random

from kafka import KafkaProducer

from core.settings import settings
from db.pg_client import PostgresClient
from event_generator import EventGenerator


class EventLoader:
    _connection = f'{settings.kafka.host}:{settings.kafka.port}'

    def __init__(self):
        self._pg_instance = PostgresClient()
        self._generator = EventGenerator(self._pg_instance)

    async def kafka_client(self):
        producer = KafkaProducer(
            bootstrap_servers=[self._connection]
        )
        try:
            yield producer
        finally:
            producer.close()

    async def load(self):
        await self._generator.get_films()

        counter = 1
        async for producer in self.kafka_client():
            while True:
                try:
                    event_func = random.choice(self._generator.events_generators)
                    event = event_func()
                    producer.send(topic='events', key=event.user_uuid, value=event.json())
                    logging.info(f"Отправлено событие #{counter} {event.json()}")
                except Exception as e:
                    logging.warning(f"Ошибка при отправке события #{counter} {event.json()}")
                finally:
                    counter += 1
                    await asyncio.sleep(2)
