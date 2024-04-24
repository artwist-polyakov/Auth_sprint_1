import uuid
from uuid import UUID

from pydantic import BaseModel, Field


class MongoBookmark(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    user_uuid: str
    film_id: str
    timestamp: int

