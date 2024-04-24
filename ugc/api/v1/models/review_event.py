import time
import uuid

from pydantic import BaseModel, Field


class ReviewEventSchema(BaseModel):
    id: str = str(uuid.uuid4())
    user_uuid: str = ...
    film_id: str = ...
    content: str = Field(..., min_length=1, max_length=1000)
    timestamp: int = time.time_ns()


class EditReviewEventSchema(BaseModel):
    id: str = ...
    user_uuid: str = ...
    film_id: str = ...
    content: str = Field(..., min_length=1, max_length=1000)
    timestamp: int = time.time_ns()


class DeleteReviewEvent(BaseModel):
    user_uuid: str = ...
    id: str = ...
    timestamp: int = time.time_ns()


class GetUserReviewsEvent(BaseModel):
    user_uuid: str
