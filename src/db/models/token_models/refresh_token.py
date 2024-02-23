from uuid import UUID

from pydantic import BaseModel


class RefreshToken(BaseModel):
    uuid: UUID
    user_id: UUID
    active_till: int
