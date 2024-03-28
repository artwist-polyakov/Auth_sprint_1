from abc import ABC, abstractmethod

from utils.abstract_utils import SingletonMeta


class AbstractMessageBrokerStorage(ABC, metaclass=SingletonMeta):

    @abstractmethod
    async def producer(self, topic, value, key) -> str:
        ...

    @abstractmethod
    async def consumer(self, topic, connection, auto_offset_reset, group_id):
        ...
