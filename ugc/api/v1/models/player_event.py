from pydantic import BaseModel


class PlayerEvent(BaseModel):
    user_uuid: str
    film_uuid: str
    event_type: str
    timestamp: int
