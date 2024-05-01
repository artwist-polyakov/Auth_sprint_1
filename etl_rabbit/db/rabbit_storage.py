import pika

from core.settings import get_settings


class RabbitCore:
    def __init__(self):
        self.host = get_settings().rabbit.host
        self.port = get_settings().rabbit.port
        self.username = get_settings().rabbit.username
        self.password = get_settings().rabbit.password
        self.connection = None
        self.channel = None

    def __enter__(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def create_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name)
