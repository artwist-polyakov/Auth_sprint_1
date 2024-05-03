import logging

from db.storage.postgres_storage import PostgresStorage

logger = logging.getLogger('etl-tasks-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

storage = PostgresStorage()
tasks = storage.getNewTasks()

logger.info("ETL started")

for task in tasks:
    logger.info(f"Task {task.id} is launched: {task.is_launched}")
