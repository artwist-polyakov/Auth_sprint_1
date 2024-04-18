from uuid import UUID

from pydantic import BaseModel

from .mixin import TimeStampWithUUIDMixin


class Critique(BaseModel, TimeStampWithUUIDMixin):
    user_id: UUID
    film_id: UUID
    rating: int
    content: str
