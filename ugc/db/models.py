from uuid import UUID

from db.mixins import UUIDMixin
from sqlmodel import Field, SQLModel


class UgcSqlModel(SQLModel):
    ...


class Click(UgcSqlModel, UUIDMixin):
    user_id: UUID = Field(nullable=False)
