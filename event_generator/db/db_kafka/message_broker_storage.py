from abc import ABC, abstractmethod

from db.db_kafka.models.kafka_models import KafkaModel
from utils.abstract_utils import SingletonMeta


class MessageBrokerProducer(ABC, metaclass=SingletonMeta):

    @abstractmethod
    def produce(self, data: KafkaModel):  # , topic, value, key) -> str:
        ...


class MessageBrokerConsumer(ABC, metaclass=SingletonMeta):

    @abstractmethod
    async def consume(self, data: dict):  # , topic, connection, auto_offset_reset):
        ...
