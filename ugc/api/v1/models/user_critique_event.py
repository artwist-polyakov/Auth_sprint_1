from uuid import UUID

from pydantic import BaseModel


class UserCritiqueEventSchema(BaseModel):
    user_id: UUID
    critique_id: UUID
