import logging
import traceback
from functools import lru_cache, wraps

from core.settings import settings
from kafka import KafkaConsumer

from db.message_broker_storage import MessageBrokerConsumer


class KafkaCore:

    _connection = f'{settings.kafka.host}:{settings.kafka.port}'
    _auto_offset_reset = 'earliest'
    _topics = ['player_events', 'view_events', 'custom_events']


class KafkaRepository(KafkaCore, MessageBrokerConsumer):
    async def consume(self):
        try:
            return KafkaConsumer(
                *self._topics,
                bootstrap_servers=[self._connection],
                auto_offset_reset=self._auto_offset_reset
            )
        except Exception as e:
            print(e)
            raise e


@lru_cache
def get_kafka():
    return KafkaRepository()
