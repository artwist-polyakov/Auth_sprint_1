from queue.base_queue import BaseQueue
from typing import Any, Callable

import pika
from configs.settings import get_settings
from models.task_result import TaskResult


class RabbitQueue(BaseQueue):
    def __init__(self):
        self.host = get_settings().rabbit.host
        self.port = get_settings().rabbit.amqp_port
        self.username = get_settings().rabbit.user
        self.password = get_settings().rabbit.password
        self.connection = None
        self.channel = None

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

    def push(self, task: TaskResult, queue, session=None) -> bool:
        with self:
            self.channel.confirm_delivery()
            properties = pika.BasicProperties(
                delivery_mode=2,
                headers={"Task-Id": str(task.id)}
            )
            self.channel.basic_publish(
                exchange=get_settings().get_rabbit_settings().exchange,
                routing_key=queue,
                body=str(task.model_dump()),
                properties=properties
            )

    def pop(self, queue, handler: Callable[[Any, Any, Any, bytes], None]):
        with self:
            method_frame, header_frame, body = self.channel.basic_get(
                queue=queue,
                auto_ack=True,
                on_message_callback=handler
            )

    def close(self):
        pass
