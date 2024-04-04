from api.v1.models.custom_event import CustomEvent
from api.v1.models.player_event import PlayerEvent
from api.v1.models.view_event import ViewEvent
from db.queue.models.kafka_models import KafkaModel
from pydantic import BaseModel


class EventConvertor:
    @staticmethod
    def map(event: BaseModel) -> KafkaModel:
        match (event):
            case PlayerEvent() as e:
                topic = "player_events"
            case ViewEvent() as e:
                topic = "view_events"
            case CustomEvent() as e:
                topic = "custom_events"
            case _:
                raise ValueError("Unknown event type")
        content = e.json()
        return KafkaModel(topic=topic, key=event.user_uuid, value=content)
