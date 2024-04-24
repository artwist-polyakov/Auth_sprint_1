from api.v1.models.bookmark_event import AddBookmarkEvent, DeleteBookmarkEvent
from api.v1.models.custom_event import CustomEvent
from api.v1.models.player_event import PlayerEvent
from api.v1.models.rate_event import (DeleteRateEvent, RateMovieSchema,
                                      RateReviewSchema)
from api.v1.models.review_event import (DeleteReviewEvent,
                                        EditReviewEventSchema,
                                        ReviewEventSchema)
from api.v1.models.view_event import ViewEvent
from db.queue.models.kafka_models import KafkaModel
from pydantic import BaseModel


class EventConvertor:
    @staticmethod
    def map(event: BaseModel) -> KafkaModel:
        match(event):
            # EVENTS TOPICS
            case PlayerEvent() as e:
                topic = "player_events"
            case ViewEvent() as e:
                topic = "view_events"
            case CustomEvent() as e:
                topic = "custom_events"

            # CONTENT TOPICS
            case DeleteBookmarkEvent() as e:
                topic = "delete_bookmark_events"
            case AddBookmarkEvent() as e:
                topic = "add_bookmark_events"
            case ReviewEventSchema() | EditReviewEventSchema() as e:
                topic = "review_events"
            case DeleteReviewEvent() as e:
                topic = "delete_review_events"
            case RateMovieSchema() as e:
                topic = "rate_movie_events"
            case RateReviewSchema() as e:
                topic = "rate_review_events"
            case DeleteRateEvent() as e:
                topic = "delete_rate_events"
            case _:
                raise ValueError("Unknown event type")
        content = e.model_dump_json()
        return KafkaModel(topic=topic, key=event.user_uuid, value=content)
