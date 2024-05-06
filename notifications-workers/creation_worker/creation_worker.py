import ast
import logging
import os
import signal
import sys

from configs.settings import get_settings
from db.storage.postgres_storage import PostgresStorage
from models.enriching_message import EnrichingMessageTask
from models.message import Message
from models.single_task import SingleTask
from queues.rabbit_queue import RabbitQueue

logger = logging.getLogger('creating-worker-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

worker_id = os.getenv("WORKER_ID", "worker_unknown")
rabbitmq_tasks = RabbitQueue(get_settings().get_rabbit_settings().tasks_queue)
rabbitmq_notifications = RabbitQueue(get_settings().get_rabbit_settings().notifications_key)
rabbitmq_enriched = RabbitQueue(get_settings().rabbit.enriched_key)
storage = PostgresStorage()


def handle_exit(sig, frame):
    print(f"{worker_id} received signal to terminate.")
    sys.exit(0)


def handler(ch, method, properties, body):
    try:
        data = Message(**ast.literal_eval(body.decode()))
        task = SingleTask(**data.model_dump())
        logger.info(f"Processing task | creation_worker | {data}")
        for user_id in data.user_ids:
            task.user_id = user_id
            task.task_id = data.id

            created_notification = storage.save_notification(task)

            task.id = created_notification.id

            if task.type == "email":
                rabbitmq_notifications.push(message=task)
            else:
                task = EnrichingMessageTask(**task.model_dump(), contact="websocket")
                rabbitmq_enriched.push(message=task)

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error in callback: {e}")
        sys.stdout.flush()


signal.signal(signal.SIGTERM, handle_exit)

try:
    rabbitmq_tasks.pop(handler=handler)
except Exception as e:
    print(f"{worker_id} encountered an error: {e}")
    sys.stdout.flush()  # Принудительно записываем лог
    sys.exit(1)
