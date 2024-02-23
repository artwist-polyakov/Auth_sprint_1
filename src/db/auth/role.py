import uuid

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from configs.settings import settings

Base = declarative_base()


class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = {'schema': f'{settings.postgres_schema_2}'}

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    name = Column(String(255), unique=True, nullable=False)
    is_verified = Column(Boolean, default=0, nullable=False)

    def __init__(self,
                 name: str,
                 is_verified: bool) -> None:
        self.name = name
        self.is_verified = is_verified

    def __repr__(self) -> str:
        return f'<Role {self.name}>'
