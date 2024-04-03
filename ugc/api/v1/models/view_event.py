import time
from typing import List

from pydantic import BaseModel, Field


class ViewEvent(BaseModel):
    user_uuid: str
    film_uuid: str
    timestamp: int = time.monotonic_ns()


class ListOfViewEvents(BaseModel):
    events: List[ViewEvent] = Field(..., description="List of view events")
