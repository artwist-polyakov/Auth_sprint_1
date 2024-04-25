import uuid

from beanie import Document, Indexed
from pydantic import Field


class BeanieFilm(Document):
    id: Indexed(str) = Field(default_factory=lambda: str(uuid.uuid4()))
    likes_counter: int = 0
    rating: float = 0.0

    class Settings:
        name = "films"
