from functools import lru_cache

import kafka
from core.settings import get_settings
from db.message_broker_storage import MessageBrokerConsumer
from kafka import KafkaConsumer, OffsetAndMetadata


class KafkaCore:
    _connection = f'{get_settings().kafka.host}:{get_settings().kafka.port}'
    _auto_offset_reset = 'earliest'
    _topics = ["delete_bookmark_events",
               "add_bookmark_events",
               "review_events",
               "delete_review_events",
               "rate_movie_events",
               "rate_review_events",
               "delete_film_rate_events",
               "delete_review_rate_events",]


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
