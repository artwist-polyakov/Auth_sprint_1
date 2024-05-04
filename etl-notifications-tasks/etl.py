import logging
from queue.rabbit_queue import RabbitQueue

from configs.settings import get_settings
from db.storage.postgres_storage import PostgresStorage

logger = logging.getLogger('etl-tasks-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

storage = PostgresStorage()
rabbitmq_tasks = RabbitQueue(
    get_settings().get_rabbit_settings().tasks_key
)
logger.info("ETL started")
tasks = storage.get_new_tasks()


for task in tasks:
    logger.info(f"Processing task {task.id}")
    rabbitmq_tasks.push(task)
    storage.mark_task_as_launched(task.id)
    logger.info(f"Task {task.id} processed")
