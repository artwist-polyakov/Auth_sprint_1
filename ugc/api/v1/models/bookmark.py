from pydantic import BaseModel

from .mixin import TimeStampWithUUIDMixin

# TODO удалить


class Bookmark(BaseModel, TimeStampWithUUIDMixin):
    user_id: str
    film_id: str
