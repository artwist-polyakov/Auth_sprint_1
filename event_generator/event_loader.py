import asyncio
import logging
import random

from db.db_kafka.kafka_storage import get_kafka
from db.db_kafka.models.kafka_models import KafkaModel
from db.pg_client import PostgresClient
from event_generator import EventGenerator

from db.models import Click, PlayerEvent, OtherEvent


class EventLoader:
    def __init__(self):
        self._pg_instance = PostgresClient()
        self._generator = EventGenerator(self._pg_instance)
        self._kafka = get_kafka()

    async def load(self):
        await self._generator.get_films()

        counter = 1
        while True:
            try:
                event_func = random.choice(self._generator.events_generators)
                event = event_func()
                match event:
                    case PlayerEvent():
                        topic = 'player_events'
                    case Click():
                        topic = 'click_events'
                    case OtherEvent():
                        topic = 'other_events'
                    case _:
                        raise ValueError('Unknown event type')
                data = KafkaModel(topic=topic, key=str(event.user_id), value=event.json())
                self._kafka.produce(data)
            except Exception as e:
                logging.warning(f"Ошибка при отправке события #{counter}")
            finally:
                counter += 1
                await asyncio.sleep(2)
