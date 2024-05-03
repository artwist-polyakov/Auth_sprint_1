import uuid

import pika
from core.settings import get_settings


class RabbitCore:
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

    def create_queue(self, queue_name: str):
        self.channel.queue_declare(queue=queue_name, durable=True)

    def send_message(self, queue_name: str, message: str):
        self.channel.confirm_delivery()
        properties = pika.BasicProperties(
            delivery_mode=2,
            headers={"X-Request-Id": str(uuid.uuid4())}
        )
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=properties
        )
