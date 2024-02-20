import uuid

from pydantic import BaseModel


class AccessTokenContainer(BaseModel):
    user_id: uuid.UUID
    role: list[str]
    verified: bool = False
    subscribed: bool = False
    subscription_till: int = 0
    created_at: int = 0
    refresh_id: uuid.UUID
