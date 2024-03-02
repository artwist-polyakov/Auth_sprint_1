from pydantic import BaseModel


class AccessTokenContainer(BaseModel):
    user_id: str
    role: str
    is_superuser: bool = False
    verified: bool = False
    subscribed: bool = False
    subscribed_till: int = 0
    created_at: int = 0
    refresh_id: str
    refreshed_at: int = 0
    user_device_type: str
