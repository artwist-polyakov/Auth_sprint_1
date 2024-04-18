from datetime import datetime
from uuid import UUID


class UUIDMixin:
    uuid: UUID


class TimeStampMixin:
    updated: datetime
    created: datetime


class TimeStampWithUUIDMixin(TimeStampMixin, UUIDMixin):
    ...
