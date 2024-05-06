import ast
import asyncio
import logging
import os
import signal
import sys

from configs.settings import get_settings
from db.pg_client import PostgresClient
from models.enriching_message import EnrichingMessageTask
from models.single_task import SingleTask
from queues.rabbit_queue import RabbitQueue

logger = logging.getLogger('creating-worker-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

worker_id = os.getenv("WORKER_ID", "worker_unknown")
rabbitmq_notifications = RabbitQueue(get_settings().rabbit.notifications_queue)
rabbitmq_enriched = RabbitQueue(get_settings().rabbit.enriched_key)

loop = asyncio.get_event_loop()
user_storage = PostgresClient()


def handle_exit(sig, frame):
    print(f"{worker_id} received signal to terminate.")
    sys.exit(0)


def handler(ch, method, properties, body):
    try:
        data = SingleTask(**ast.literal_eval(body.decode()))

        # тут мы получаем contact пользователя по типу
        # (мейл, телефон или ws_id) и обогащаем task новыми данными
        # нужно добить получение пользователя
        # user = loop.run_until_complete(user_storage.get_user(user_id=data.user_id))
        # print(f"!!!!!!!!!!!!!!!!!!!!!user = {user}")
        # sys.stdout.flush()  # Принудительно записываем лог

        task = EnrichingMessageTask(**data.model_dump(), contact="samtonck@gmail.com")
        logger.info(f"Processing task | enriching_worker | {task}")
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
