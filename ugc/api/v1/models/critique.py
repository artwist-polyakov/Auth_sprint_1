from pydantic import BaseModel, model_validator
from typing_extensions import Self

from .mixin import TimeStampWithUUIDMixin


class Critique(BaseModel, TimeStampWithUUIDMixin):
    user_id: str
    film_id: str
    rating: int | None = None
    content: str | None = None

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        rating = self.rating
        content = self.content
        if rating is None and content is None:
            raise ValueError('at less rating or content should be provided')
        return self
