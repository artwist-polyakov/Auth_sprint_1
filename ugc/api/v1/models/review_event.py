from pydantic import BaseModel, Field


class ReviewEventSchema(BaseModel):
    user_id: str = ...
    content: str = Field(..., min_length=1, max_length=1000)


class DeleteReviewEvent(BaseModel):
    user_id: str
    film_id: str


class GetUserReviewsEvent(BaseModel):
    user_id: str
