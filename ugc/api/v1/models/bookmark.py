from uuid import UUID

from pydantic import BaseModel

from .mixin import TimeStampWithUUIDMixin


class Bookmark(BaseModel, TimeStampWithUUIDMixin):
    user_id: UUID
    film_id: UUID
