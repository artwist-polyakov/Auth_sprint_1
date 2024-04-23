import time

from pydantic import BaseModel


class GetUserBookmarksEvent(BaseModel):
    user_uuid: str


class DeleteBookmarkEvent(BaseModel):
    user_uuid: str
    film_id: str


class AddBookmarkEvent(BaseModel):
    user_uuid: str
    film_id: str
    timestamp: int = time.time_ns()
