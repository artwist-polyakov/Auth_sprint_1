import time
from typing import List, Optional

from pydantic import BaseModel, Field


class ViewEvent(BaseModel):
    user_uuid: Optional[str] = None
    film_uuid: str
    timestamp: int = time.time_ns()


class ListOfViewEvents(BaseModel):
    events: List[ViewEvent] = Field(..., description="List of view events")
