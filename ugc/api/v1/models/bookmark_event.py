from pydantic import BaseModel


class GetUserBookmarksEvent(BaseModel):
    user_id: str


class DeleteBookmarkEvent(BaseModel):
    user_id: str
    film_id: str
