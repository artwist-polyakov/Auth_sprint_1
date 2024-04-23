from pydantic import BaseModel, Field


class RateMovieSchema(BaseModel):
    rating: int = Field(..., ge=1, le=10)
    user_id: str
    film_id: str


class RateReviewSchema(BaseModel):
    rating: int = Field(..., ge=1, le=10)
    user_id: str = ...
    review_id: str = ...


class DeleteRateEvent(BaseModel):
    user_id: str
    film_id: str


class GetRatedFilmsEvent(BaseModel):
    user_id: str


class GetRatedReviewsEvent(BaseModel):
    user_id: str


class GetFilmRatingEvent(BaseModel):
    film_id: str
