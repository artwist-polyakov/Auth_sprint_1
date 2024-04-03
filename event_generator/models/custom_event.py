from pydantic import BaseModel


class CustomEvent(BaseModel):
    user_uuid: str
    event_type: str
    timestamp: int
