import time

from pydantic import BaseModel, Field


class RateMovieSchema(BaseModel):
    rating: int = Field(..., ge=1, le=10)
    user_uuid: str
    film_id: str
    timestamp: int = time.time_ns()


class RateReviewSchema(BaseModel):
    rating: int = Field(..., ge=1, le=10)
    user_uuid: str = ...
    review_id: str = ...
    timestamp: int = time.time_ns()


class DeleteRateEvent(BaseModel):
    user_uuid: str
    film_id: str


class GetRatedFilmsEvent(BaseModel):
    user_uuid: str


class GetRatedReviewsEvent(BaseModel):
    user_uuid: str


class GetFilmRatingEvent(BaseModel):
    film_id: str
