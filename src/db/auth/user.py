import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from werkzeug.security import check_password_hash, generate_password_hash

from configs.settings import settings


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': f'{settings.postgres_schema_2}'}

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    is_verified = Column(Boolean, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self,
                 login: str,
                 password: str,
                 first_name: str,
                 last_name: str,
                 is_verified: bool) -> None:
        self.login = login
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_verified = is_verified

    def __repr__(self) -> str:
        return f'<User {self.login}>'
