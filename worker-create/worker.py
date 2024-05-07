import ast
import logging
import os
import signal
import sys
from types import FrameType

from configs.settings import get_settings
from db.storage.postgres_storage import PostgresStorage
from models.enriching_message import EnrichingMessageTask
from models.message import Message
from models.single_task import SingleTask
from pika.channel import Channel
from pika.spec import Basic, BasicProperties
from queues.rabbit_queue import RabbitQueue

logger = logging.getLogger('creating-worker-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

rabbitmq_tasks = RabbitQueue(get_settings().get_rabbit_settings().tasks_queue)
rabbitmq_notifications = RabbitQueue(get_settings().get_rabbit_settings().notifications_key)
rabbitmq_enriched = RabbitQueue(get_settings().rabbit.enriched_key)
storage = PostgresStorage()


def handler(
        ch: Channel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes
):
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


try:
    rabbitmq_tasks.pop(handler=handler)
except Exception as e:
    logger.error(f"Error in worker: {e}")
