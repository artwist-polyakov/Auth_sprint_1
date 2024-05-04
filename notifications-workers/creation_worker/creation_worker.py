import ast
import logging
import os
import signal
import sys
from queue.rabbit_queue import RabbitQueue

from configs.settings import get_settings
from models.message import Message
from models.single_task import SingleTask

logger = logging.getLogger('creating-worker-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

worker_id = os.getenv("WORKER_ID", "worker_unknown")
rabbitmq_tasks = RabbitQueue(get_settings().rabbit.tasks_queue)
rabbitmq_notifications = RabbitQueue(get_settings().get_rabbit_settings().notifications_key)



def handle_exit(sig, frame):
    print(f"{worker_id} received signal to terminate.")
    sys.exit(0)


def handler(ch, method, properties, body):
    try:
        data = Message(**ast.literal_eval(body.decode()))
        task = SingleTask(**data.model_dump())
        logger.info(f"Processing task {data}")
        for user_id in data.user_ids:
            task.user_id = user_id
        rabbitmq_notifications.push(message=task)
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