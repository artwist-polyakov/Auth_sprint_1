import ast
import logging
import os
import signal
import sys
from queue.rabbit_queue import RabbitQueue

from configs.settings import get_settings
from models.enriching_message import EnrichingMessageTask

logger = logging.getLogger('creating-worker-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

worker_id = os.getenv("WORKER_ID", "worker_unknown")
rabbitmq_to_sending = RabbitQueue(get_settings().rabbit.to_sending_queue)


def handle_exit(sig, frame):
    print(f"{worker_id} received signal to terminate.")
    sys.exit(0)


def handler(ch, method, properties, body):
    try:
        data = EnrichingMessageTask(**ast.literal_eval(body.decode()))
        logger.info(f"Processing task {worker_id} | {data}")

        # тут мы отсылаем сообщение пользователю

    except Exception as e:
        print(f"Error in callback: {e}")
        sys.stdout.flush()


signal.signal(signal.SIGTERM, handle_exit)

try:
    rabbitmq_to_sending.pop(handler=handler)
except Exception as e:
    print(f"{worker_id} encountered an error: {e}")
    sys.stdout.flush()  # Принудительно записываем лог
    sys.exit(1)
