from datetime import datetime, timezone
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field, model_validator


class BeanieBookmark(Document):
    id: UUID = Field(default_factory=uuid4)
    user_uuid: Indexed(str)
    film_id: Indexed(str)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "bookmarks"

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
