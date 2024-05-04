import os
import signal
import sys
from queue.rabbit_queue import RabbitQueue

worker_id = os.getenv("WORKER_ID", "worker_unknown")
read_queue_name = os.getenv("RABBIT_MQ_TASKS_KEY", "tasks")
write_queue_name = os.getenv("RABBIT_MQ_ENRICHED_KEY", "enriched")
rabbitmq_tasks = RabbitQueue()


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
        rabbitmq_tasks.pop(queue=read_queue_name, handler=callback)
        # rabbitmq_tasks.push(message={"id": 123412341234}, queue=write_queue_name)
except Exception as e:
    print(f"{worker_id} encountered an error: {e}")
    sys.stdout.flush()  # Принудительно записываем лог
    sys.exit(1)
