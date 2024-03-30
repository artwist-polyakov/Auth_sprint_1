import logging
from functools import lru_cache

from core.settings import settings
from kafka import KafkaConsumer, KafkaProducer

from schemas.kafka import KafkaRepositoryProducerSchema, KafkaRepositoryConsumerSchema
from services.kafka.message_broker_storage import MessageBrokerProducer, MessageBrokerConsumer


class KafkaCore:
    _connection = f'{settings.kafka.host}:{settings.kafka.port}'

    async def close(self):
        ...


class KafkaRepository(KafkaCore, MessageBrokerProducer, MessageBrokerConsumer):

    async def producer(self, data: KafkaRepositoryProducerSchema):
        try:
            producer = KafkaProducer(bootstrap_servers=[self._connection])
            return producer.send(
                topic=data.topic,
                key=data.key.encode('UTF-8'),
                value=data.value.encode('UTF-8')
            )
        except Exception as e:
            logging.info(e)
            raise e

    async def consumer(self, data: KafkaRepositoryConsumerSchema, auto_offset_reset='earliest'):
        try:
            if data.auto_offset_reset:
                auto_offset_reset = data.auto_offset_reset

            return KafkaConsumer(
                topic=data.topic,
                bootstrap_servers=[self._connection],
                auto_offset_reset=auto_offset_reset,
                group_id=data.group_id
            )
        except Exception as e:
            logging.info(e)
            raise e


@lru_cache
def get_kafka():
    return KafkaRepository()
