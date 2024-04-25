from uuid import UUID

from pydantic import BaseModel


class UserBookmarksEventSchema(BaseModel):
    user_id: UUID
    film_ids: UUID
