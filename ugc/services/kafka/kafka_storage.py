import logging
from abc import ABC

from core.settings import settings
from kafka import KafkaConsumer, KafkaProducer
from services.kafka.message_broker_storage import AbstractMessageBrokerStorage


class KafkaStorage(AbstractMessageBrokerStorage, ABC):
    connection = f'{settings.kafka.host}:{settings.kafka.port}'

    async def write_message(self, topic, key, value):
        try:
            producer = KafkaProducer(bootstrap_servers=[self.connection])
            return producer.send(topic=topic, key=key.encode('UTF-8'), value=value.encode('UTF-8'))
        except Exception as e:
            logging.info(e)
            raise e

    async def read_message(self, topic, group_id, auto_offset_reset='earliest'):
        try:
            return KafkaConsumer(
                topic=topic,
                bootstrap_servers=[self.connection],
                auto_offset_reset=auto_offset_reset,
                group_id=group_id
            )
        except Exception as e:
            logging.info(e)
            raise e
