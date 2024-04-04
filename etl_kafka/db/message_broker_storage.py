from abc import ABC, abstractmethod


class MessageBrokerConsumer(ABC):

    @abstractmethod
    async def consume(self):  # , topic, connection, auto_offset_reset):
        ...
