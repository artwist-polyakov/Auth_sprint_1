from uuid import UUID

from db.mixins import TimeStampWithUUID
from sqlmodel import Field, SQLModel


class UgcSqlModel(SQLModel):
    ...


class Click(UgcSqlModel, TimeStampWithUUID):
    user_id: UUID = Field(nullable=False)
    movie_id: UUID = Field(nullable=False)


class PlayerEvent(UgcSqlModel, TimeStampWithUUID):
    user_id: UUID = Field(nullable=False)
    movie_id: UUID = Field(nullable=False)
    type: str = Field(nullable=False)
    depth: int = Field(nullable=False)


class OtherEvent(UgcSqlModel, TimeStampWithUUID):
    user_id: UUID = Field(nullable=False)
    movie_id: UUID = Field(nullable=False)
    type: str = Field(nullable=False)


class Critique(UgcSqlModel, TimeStampWithUUID):
    rating: str = Field(nullable=False)
    content: str = Field(nullable=False)


class UserCritique(UgcSqlModel, TimeStampWithUUID):
    user_id: UUID = Field(nullable=False)
    critique_id: UUID = Field(nullable=False)


class Film(UgcSqlModel, TimeStampWithUUID):
    film_id: UUID = Field(nullable=False)
    critique_ids: list[UUID] = Field(nullable=False)
    film_rating: float = Field(nullable=False)


class UserBookmarks(UgcSqlModel, TimeStampWithUUID):
    user_id: UUID = Field(nullable=False)
    film_ids: list[UUID] = Field(nullable=False)
