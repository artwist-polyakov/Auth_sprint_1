from pydantic import BaseModel


class ViewEvent(BaseModel):
    user_uuid: str
    film_uuid: str
