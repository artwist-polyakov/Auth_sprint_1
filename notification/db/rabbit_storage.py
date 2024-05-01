import pika
import time
import uuid
from core.settings import get_settings


class RabbitMQCore:
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(
            get_settings().rabbit.username,
            get_settings().rabbit.password
        )
        parameters = pika.ConnectionParameters(
            host=get_settings().rabbit.host,
            port=get_settings().rabbit.port,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

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

    def disconnect(self):
        self.connection.close()
