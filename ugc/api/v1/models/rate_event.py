import time

from pydantic import BaseModel, Field


class RateMovieSchema(BaseModel):
    rate: int = Field(..., ge=0, le=10)
    user_uuid: str
    film_id: str
    timestamp: int = time.time_ns()


class RateReviewSchema(BaseModel):
    rate: int = Field(..., ge=0, le=10)
    user_uuid: str = ...
    review_id: str = ...
    timestamp: int = time.time_ns()


class DeleteFilmRateEvent(BaseModel):
    rate_id: str
    user_uuid: str
    timestamp: int = time.time_ns()


class DeleteReviewRateEvent(BaseModel):
    rate_id: str
    user_uuid: str
    timestamp: int = time.time_ns()


class GetRatedFilmsEvent(BaseModel):
    user_uuid: str


class GetRatedReviewsEvent(BaseModel):
    user_uuid: str


class GetFilmRatingEvent(BaseModel):
    film_id: str
