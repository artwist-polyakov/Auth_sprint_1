from typing import Callable, TypeVar

import pika
from configs.settings import get_settings
from queues.base_queue import BaseQueue

T = TypeVar('T')


class RabbitQueue(BaseQueue):
    def __init__(self, key: str):
        self.host = get_settings().rabbit.host
        self.port = get_settings().rabbit.amqp_port
        self.username = get_settings().rabbit.user
        self.password = get_settings().rabbit.password
        self.connection = None
        self.channel = None
        self._key = key

    def __enter__(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def push(self, message: T, session=None) -> bool:
        with self:
            self.channel.confirm_delivery()
            properties = pika.BasicProperties(
                delivery_mode=2,
                headers={"Task-Id": str(message.id)}
            )
            self.channel.basic_publish(
                exchange=get_settings().get_rabbit_settings().exchange,
                routing_key=self._key,
                body=str(message.model_dump()),
                properties=properties
            )

    def pop(self,
            handler: Callable[
                [pika.channel.Channel,
                 pika.spec.Basic.Deliver,
                 pika.spec.BasicProperties,
                 bytes],
                None
            ]):
        with self:
            self.channel.basic_consume(
                queue=self._key,
                on_message_callback=handler,
                auto_ack=False
            )
            self.channel.start_consuming()

    def close(self):
        pass
