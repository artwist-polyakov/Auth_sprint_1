from uuid import UUID, uuid4

from sqlmodel import Field


class UUIDMixin:
    """Класс-миксин UUID id первичный ключ."""

    id: UUID = Field(primary_key=True, default_factory=uuid4, nullable=False)
