from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Movie(BaseModel):
    id: UUID
    title: str
    description: str | None
    imdb_rating: float | None
    genre: list[str]
    modified: datetime
    created: datetime
    director: list[str]
    actors_names: list[str]
    writers_names: list[str]
