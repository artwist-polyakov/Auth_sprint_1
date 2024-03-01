import uuid

from configs.settings import settings
from db.auth.base import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID


class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = {'schema': settings.postgres_schema_2}

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    role = Column(String(255), nullable=False)
    resource = Column(String(255), nullable=False)
    verb = Column(String(255), nullable=False)

    def __init__(self,
                 uuid: str,
                 role: str,
                 resource: str,
                 verb: str) -> None:
        self.uuid = uuid
        self.role = role
        self.resource = resource
        self.verb = verb

    def __repr__(self) -> str:
        return f'<Role {self.role}>'
