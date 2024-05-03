import logging
from queue.rabbit_queue import RabbitQueue

from db.storage.postgres_storage import PostgresStorage

logger = logging.getLogger('etl-tasks-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

storage = PostgresStorage()
rabbitmq = RabbitQueue()

tasks = storage.getNewTasks()

logger.info("ETL started")

for task in tasks:
    logger.info(f"Processing task {task.id}")
    rabbitmq.push(task)
    storage.markTaskLaunched(task.id)
    logger.info(f"Task {task.id} processed")
