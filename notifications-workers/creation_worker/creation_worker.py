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
        data = Message(**json.loads(body.decode()))  # валидируем через пайдантик пришедшие данные
        user_ids_list = deepcopy(data.user_ids)  # получаем список id
        del data.user_ids  # удаляем поле из даты

        for user_id in user_ids_list:
            data_single_task = SingleTask(user_id=user_id, **data.__dict__)
            rabbitmq_notifications.push(message=data_single_task)
    except Exception as e:
        print(f"Error in callback: {e}")
        sys.stdout.flush()  # Принудительно записываем лог


signal.signal(signal.SIGTERM, handle_exit)

try:
    rabbitmq_tasks.pop(handler=handler)
except Exception as e:
    print(f"{worker_id} encountered an error: {e}")
    sys.stdout.flush()  # Принудительно записываем лог
    sys.exit(1)
