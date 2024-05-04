import ast
import logging
import os
import signal
import sys
from queue.rabbit_queue import RabbitQueue

from configs.settings import get_settings
from models.enriching_message import EnrichingMessageTask
from models.single_task import SingleTask

logger = logging.getLogger('creating-worker-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

worker_id = os.getenv("WORKER_ID", "worker_unknown")
rabbitmq_notifications = RabbitQueue(get_settings().rabbit.notifications_queue)
rabbitmq_enriched = RabbitQueue(get_settings().get_rabbit_settings().enriched_key)


def handle_exit(sig, frame):
    print(f"{worker_id} received signal to terminate.")
    sys.exit(0)


def handler(ch, method, properties, body):
    try:
        data = SingleTask(**ast.literal_eval(body.decode()))
        task = EnrichingMessageTask(**data.model_dump())
        logger.info(f"Processing task {worker_id} | {data}")

        # тут мы получаем contact пользователя по типу
        # (мейл, телефон или ws_id) и template (тело сообщения)
        # и обогащаем task новыми данными

        rabbitmq_enriched.push(message=task)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error in callback: {e}")
        sys.stdout.flush()


signal.signal(signal.SIGTERM, handle_exit)

try:
    rabbitmq_notifications.pop(handler=handler)
except Exception as e:
    print(f"{worker_id} encountered an error: {e}")
    sys.stdout.flush()  # Принудительно записываем лог
    sys.exit(1)
