import logging
from functools import lru_cache
from http import HTTPStatus

from db.queue.kafka_repository import get_kafka
from pydantic import BaseModel
from services.base_service import BaseService
from services.event_convertor import EventConvertor


class QueueService(BaseService):
    def process_event(self, event: BaseModel) -> tuple[HTTPStatus, str]:
        try:
            data = EventConvertor.map(event)
            logging.warning(f'Event has been converted: {data}')
            self._queue.produce(data)
            return HTTPStatus.OK, 'Event has been processed'
        except Exception as e:
            return HTTPStatus.INTERNAL_SERVER_ERROR, str(e)


@lru_cache
def get_queue_service():
    return QueueService(get_kafka())
