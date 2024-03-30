from typing import List

from pydantic import BaseModel, Field


class ViewEvent(BaseModel):
    user_uuid: str
    film_uuid: str


class ListOfViewEvents(BaseModel):
    events: List[ViewEvent] = Field(..., description="List of view events")