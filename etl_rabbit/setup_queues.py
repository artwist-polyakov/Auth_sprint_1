from db.rabbit_storage import RabbitCore
from core.settings import get_settings

settings = get_settings()

queues = ["queue1", "queue2", "queue3"]

with RabbitCore() as rabbit:
    print(rabbit)
    for queue in queues:
        rabbit.create_queue(queue)
