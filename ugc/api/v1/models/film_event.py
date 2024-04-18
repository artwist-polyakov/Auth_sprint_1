from uuid import UUID

from pydantic import BaseModel


class FilmEventSchema(BaseModel):
    film_id: UUID
    critique_ids: list[UUID]
    film_rating: float
