import asyncio
import logging
import random

from db.db_kafka.kafka_storage import get_kafka
from db.db_kafka.models.kafka_models import KafkaModel
from db.pg_client import PostgresClient
from event_generator import EventGenerator
from models.custom_event import CustomEvent
from models.player_event import PlayerEvent
from models.view_event import ViewEvent


class EventLoader:
    def __init__(self):
        self._pg_instance = PostgresClient()
        self._generator = EventGenerator()
        self._kafka = get_kafka()

    async def load(self):

        counter = 1
        while True:
            try:
                event_func = random.choice(self._generator.events_generators)
                event = event_func()
                match event:
                    case PlayerEvent():
                        topic = 'player_events'
                    case ViewEvent():
                        topic = 'view_events'
                    case CustomEvent():
                        topic = 'custom_events'
                    case _:
                        raise ValueError('Unknown event type')
                data = KafkaModel(topic=topic, key=event.user_uuid, value=event.json())
                self._kafka.produce(data)
                logging.info(f"Отправлено событие #{counter} {event.json()}")
            except Exception as e:
                logging.warning(f"Ошибка при отправке события #{counter} {event.json()}")
            finally:
                counter += 1
                if counter % 100 == 0:
                    logging.info(f"Отправлено {counter} событий")
                    await asyncio.sleep(1)

