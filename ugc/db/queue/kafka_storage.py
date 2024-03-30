import logging
import traceback
from functools import lru_cache, wraps

from core.settings import settings
from db.queue.message_broker_storage import (MessageBrokerConsumer,
                                             MessageBrokerProducer)
from db.queue.models.kafka_models import KafkaModel
from kafka import KafkaConsumer, KafkaProducer


class KafkaCore:
    _connection = f'{settings.kafka.host}:{settings.kafka.port}'

    def __init__(self):
        self._producer = KafkaProducer(bootstrap_servers=[self._connection])

    @staticmethod
    def refresh_producer(func):
        @wraps(func)
        async def inner(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                logging.warning(f'error: {e}, {traceback.format_exc()}')
                self._producer = KafkaProducer(bootstrap_servers=[self._connection])
                return func(self, *args, **kwargs)

        return inner

    async def close(self):
        ...


class KafkaRepository(KafkaCore, MessageBrokerProducer, MessageBrokerConsumer):

    @KafkaCore.refresh_producer
    def produce(self, data: KafkaModel):
        try:
            return self._producer.send(
                topic=data.topic,
                key=data.key.encode('UTF-8'),
                value=data.value.encode('UTF-8')
            )
        except Exception as e:
            logging.warning(f'error: {e}, {traceback.format_exc()}')
            raise e

    async def consume(self, data):
        try:
            return KafkaConsumer(
                topic=data.topic,
                bootstrap_servers=[self._connection],
                auto_offset_reset=data.auto_offset_reset,
                group_id=data.group_id
            )
        except Exception as e:
            logging.info(e)
            raise e


@lru_cache
def get_kafka():
    return KafkaRepository()
