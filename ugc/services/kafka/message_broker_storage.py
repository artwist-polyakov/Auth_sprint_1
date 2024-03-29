from abc import ABC, abstractmethod

from utils.abstract_utils import SingletonMeta


class MessageBrokerProducer(ABC, metaclass=SingletonMeta):

    @abstractmethod
    async def producer(self, data: dict):  # , topic, value, key) -> str:
        ...


class MessageBrokerConsumer(ABC, metaclass=SingletonMeta):

    @abstractmethod
    async def consumer(self, data: dict):  # , topic, connection, auto_offset_reset):
        ...
