import time

from pydantic import BaseModel, Field


class ReviewEventSchema(BaseModel):
    user_uuid: str = ...
    content: str = Field(..., min_length=1, max_length=1000)
    timestamp: int = time.time_ns()


class DeleteReviewEvent(BaseModel):
    user_uuid: str
    film_id: str


class GetUserReviewsEvent(BaseModel):
    user_uuid: str
