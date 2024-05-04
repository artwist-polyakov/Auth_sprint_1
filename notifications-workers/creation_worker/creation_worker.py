import json
import os
import signal
import sys
from queue.rabbit_queue import RabbitQueue

from configs.settings import get_settings
from models.single_task import SingleTask

worker_id = os.getenv("WORKER_ID", "worker_unknown")
rabbitmq_tasks = RabbitQueue(get_settings().rabbit.tasks_queue)
rabbitmq_notifications = RabbitQueue(get_settings().get_rabbit_settings().notifications_key)


def handle_exit(sig, frame):
    print(f"{worker_id} received signal to terminate.")
    sys.exit(0)


def handler(ch, method, properties, body):
    try:
        data = json.loads(body.decode())
        for user_id in data["user_ids"]:
            data_single_task = {
                "id": data["id"],
                "title": data["title"],
                "content": data["content"],
                "user_id": user_id,
                "type": data["type"],
                "created_at": data["created_at"]
            }
            rabbitmq_notifications.push(message=SingleTask(**data_single_task))
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
