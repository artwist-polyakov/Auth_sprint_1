import logging
import traceback
from functools import lru_cache

from core.settings import settings
from db.queue.message_broker_storage import (MessageBrokerConsumer,
                                             MessageBrokerProducer)
from db.queue.models.kafka_models import KafkaModel
from kafka import KafkaConsumer, KafkaProducer


class KafkaCore:
    _connection = f'{settings.kafka.host}:{settings.kafka.port}'

    async def close(self):
        ...


class KafkaRepository(KafkaCore, MessageBrokerProducer, MessageBrokerConsumer):

    def produce(self, data: KafkaModel):
        try:
            logging.warning(f'before produce int kafka: {self._connection}')
            producer = KafkaProducer(bootstrap_servers=[self._connection])
            logging.warning('producer created')
            future = producer.send(
                topic=data.topic,
                key=data.key.encode('UTF-8'),
                value=data.value.encode('UTF-8')
            )
            # Ожидаем, пока сообщение будет отправлено
            result = future.get(timeout=10)
            logging.warning(f'after produce: {result}')
            # producer.close()
            return result
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
