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
