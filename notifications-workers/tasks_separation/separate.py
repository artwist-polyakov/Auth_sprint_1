import os
import signal
import sys
import time
from queue.rabbit_queue import RabbitQueue

from configs.settings import get_settings

worker_id = os.getenv("WORKER_ID", "worker_unknown")
rabbitmq_tasks = RabbitQueue(
    "TasksQueue"
)
rabbitmq_notifications = RabbitQueue(
    get_settings().get_rabbit_settings().notifications_key
)


def handle_exit(sig, frame):
    print(f"{worker_id} received signal to terminate.")
    sys.exit(0)


def callback(ch, method, properties, body):
    try:
        print(f" [x] Received {body.decode()}")
        sys.stdout.flush()  # Принудительно записываем лог
    except Exception as e:
        print(f"Error in callback: {e}")


signal.signal(signal.SIGTERM, handle_exit)

try:
    while True:
        print(f"{worker_id} is processing...")
        rabbitmq_tasks.pop(handler=callback)
        time.sleep(5)  # Имитация длительной работы
except Exception as e:
    print(f"{worker_id} encountered an error: {e}")
    sys.stdout.flush()  # Принудительно записываем лог
    sys.exit(1)
