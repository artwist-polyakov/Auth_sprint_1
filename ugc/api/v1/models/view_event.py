import time
from typing import List

from pydantic import BaseModel, Field


class ViewEvent(BaseModel):
    user_uuid: str | None = None
    film_uuid: str
    timestamp: int = time.time_ns()


class ListOfViewEvents(BaseModel):
    events: List[ViewEvent] = Field(..., description="List of view events")
