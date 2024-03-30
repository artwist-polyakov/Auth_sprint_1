import logging
import traceback
from functools import lru_cache, wraps

import pulsar
from db.queue.message_broker_storage import (MessageBrokerConsumer,
                                             MessageBrokerProducer)
from db.queue.models.pulsar_models import PulsarModel


class PulsarCore:
    uri = 'pulsar://localhost:6650'
    topic = 'persistent://public/default/sample'
    subscription_name = "topic-sub-1"

    def __init__(self):
        self.client = pulsar.Client(self.uri)
        self.producer = self.client.create_producer(self.topic)
        self.consumer = self.client.subscribe(self.topic, subscription_name=self.subscription_name)

    @staticmethod
    def refresh_producer(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                logging.warning(f'error: {e}, {traceback.format_exc()}')
                self.producer = self.client.create_producer(self.topic)
                return func(self, *args, **kwargs)

        return inner


class PulsarRepository(PulsarCore, MessageBrokerProducer, MessageBrokerConsumer):

    @PulsarCore.refresh_producer
    def produce(self, data: PulsarModel):
        try:
            future = self.producer.send(data.encode('UTF-8'))
            future.get(timeout=60)
            return True
        except Exception as e:
            raise e

    async def consume(self, data):
        msg = self.consumer.receive()
        try:
            return self.consumer.acknowledge(msg)
        except Exception as e:
            self.consumer.negative_acknowledge(msg)
            raise e


@lru_cache
def get_pulsar():
    return PulsarRepository()
