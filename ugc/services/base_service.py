from db.queue.message_broker_storage import MessageBrokerProducer


class BaseService:
    def __init__(self, queue: MessageBrokerProducer):
        self._queue = queue
