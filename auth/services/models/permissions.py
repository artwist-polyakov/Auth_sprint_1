from pydantic import BaseModel


class RBACInfo(BaseModel):
    role: str
    resource: str
    verb: str


class LogoutInfo(BaseModel):
    user_id: str
    refresh_id: str
