import uuid
from datetime import datetime, timezone

from beanie import Document, Indexed
from pydantic import Field, model_validator


class BeanieReview(Document):
    id: Indexed(str) = Field(default_factory=lambda: str(uuid.uuid4()))
    user_uuid: Indexed(str)
    film_id: Indexed(str) = Field("")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    rating: int = Field(0, ge=0, le=10)
    likes_counter: int = Field(0, ge=0)

    # на уровне базы данных пустая строка возможна при удалении
    content: str = Field("", min_length=0, max_length=1000)

    class Settings:
        name = "reviews"

    @model_validator(mode='before')
    def convert_ns_timestamp_to_datetime(self):
        if self['timestamp'] and isinstance(self['timestamp'], int):
            self['timestamp'] = (
                datetime.fromtimestamp(self['timestamp'] // 1_000_000_000, timezone.utc)
            )
            return self
        elif self['timestamp'] and isinstance(self['timestamp'], datetime):
            return self
        else:
            raise ValueError('Invalid timestamp value')
