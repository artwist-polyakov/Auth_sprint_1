import uuid

from beanie import Document, Indexed
from models.id_date_model import BeanieIDDate
from pydantic import Field


class BeanieUser(Document):
    id: Indexed(str) = Field(default_factory=lambda: str(uuid.uuid4()))
    bookmarks: list[BeanieIDDate] = Field(default_factory=list)
    reviews: list[BeanieIDDate] = Field(default_factory=list)
    reviews_likes: list[BeanieIDDate] = Field(default_factory=list)
    films_likes: list[BeanieIDDate] = Field(default_factory=list)

    class Settings:
        name = "users"
