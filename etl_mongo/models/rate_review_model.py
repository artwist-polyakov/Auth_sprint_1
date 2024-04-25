from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from beanie import Document, Indexed, Link
from models.review_model import BeanieReview
from pydantic import Field, model_validator


class BeanieRateReview(Document):
    id: UUID = Field(default_factory=uuid4)
    user_uuid: Indexed(str)
    review: Optional[Link[BeanieReview]] = None
    rate: int = Field(0, ge=0, le=10)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "rate_reviews"

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
