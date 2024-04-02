from api.v1.models.custom_event import CustomEvent
from api.v1.models.player_event import PlayerEvent
from api.v1.models.view_event import ViewEvent
from db.queue.models.kafka_models import KafkaModel
from pydantic import BaseModel


class EventConvertor:
    @staticmethod
    def map(event: BaseModel) -> KafkaModel:
        content = ""
        match(event):
            case PlayerEvent() | ViewEvent() | CustomEvent() as e:
                content = e.json()
            case _:
                raise ValueError("Unknown event type")
        return KafkaModel(topic="events", key=event.user_uuid, value=content)
