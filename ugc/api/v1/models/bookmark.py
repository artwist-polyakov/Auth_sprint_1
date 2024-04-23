from pydantic import BaseModel

from .mixin import TimeStampWithUUIDMixin


class Bookmark(BaseModel, TimeStampWithUUIDMixin):
    user_id: str
    film_id: str
