from sqlalchemy import BigInteger, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

from configs.settings import settings

Base = declarative_base()


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    __table_args__ = {'schema': f'{settings.postgres_schema_2}'}

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False
    )
    user_id = relationship('User', foreign_keys='user.uuid')
    active_till = Column(BigInteger, nullable=False)

    def __init__(self,
                 uuid: str,
                 user_id: str,
                 active_till: int) -> None:
        self.uuid = uuid
        self.user_id = user_id
        self.active_till = active_till
