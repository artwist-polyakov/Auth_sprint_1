from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class BaseModelWithAutoID(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()))


class Click(BaseModelWithAutoID):
    user_id: str
    movie_id: str
    created: Optional[datetime] = Field(default_factory=datetime.now)


class PlayerEvent(BaseModelWithAutoID):
    user_id: str
    movie_id: str
    type: str
    depth: int
    created: Optional[datetime] = Field(default_factory=datetime.now)


class OtherEvent(BaseModelWithAutoID):
    user_id: str
    movie_id: str
    type: str
    created: Optional[datetime] = Field(default_factory=datetime.now)
