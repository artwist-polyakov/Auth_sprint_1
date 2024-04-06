from functools import lru_cache

import kafka
from core.settings import settings
from db.message_broker_storage import MessageBrokerConsumer
from kafka import KafkaConsumer, OffsetAndMetadata


class KafkaCore:
    _connection = f'{settings.kafka.host}:{settings.kafka.port}'
    _auto_offset_reset = 'earliest'
    _topics = ['player_events', 'view_events', 'custom_events']


class KafkaRepository(KafkaCore, MessageBrokerConsumer):
    async def consume(self) -> KafkaConsumer:
        try:
            return KafkaConsumer(
                *self._topics,
                bootstrap_servers=[self._connection],
                auto_offset_reset=self._auto_offset_reset,
                enable_auto_commit=False,
                group_id='events-etl',
            )
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    async def commit(consumer: KafkaConsumer, message):
        tp = kafka.TopicPartition(message.topic, message.partition)
        consumer.commit({
            tp: OffsetAndMetadata(message.offset + 1, None)
        })


@lru_cache
def get_kafka():
    return KafkaRepository()
