import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, Field, model_validator


class BeanieIDDate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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
