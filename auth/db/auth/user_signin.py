import datetime

import uuid
from configs.settings import settings
from sqlalchemy import UniqueConstraint, Column, ForeignKey, DateTime, Text, text, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.auth.base import Base

# Список утройств (реализовано в миграции):
# ['mac_app', 'android_app', 'web', 'smart_tv']
# app может быть на телефоне и на планшете


class UserSignIn(Base):
    # !!!ВНИМАНИЕ!!!
    # ПРИ СОЗДАНИИ alembic-МИГРАЦИИ этой таблицы, НЕОБХОДИМО УДАЛИТЬ
    # из миграции строку "sa.UniqueConstraint('uuid')"

    # Иначе возникает ошибка:
    # sqlalchemy.exc.DBAPIError: (sqlalchemy.dialects.postgresql.asyncpg.Error)
    # <class 'asyncpg.exceptions.FeatureNotSupportedError'>:
    # unique constraint on partitioned table must include all partitioning columns
    # DETAIL:  UNIQUE constraint on table "user_sign_ins" lacks column "user_device_type"
    # which is part of the partition key.

    # Это связано с тем, что при создании UniqueConstraint необходимо указать и uuid, и user_device_type,
    # и это строка вызывает ошибку даже если есть вторая ПРАВИЛЬНАЯ строка, которая
    # генерируется из таблицы

    # --- Описание решения ошибки связано с тем, что его нет(?) в интернете

    __tablename__ = 'user_sign_ins'
    __table_args__ = (UniqueConstraint('uuid', 'user_device_type'),
                      {'schema': settings.postgres_schema_2,
                       'postgresql_partition_by': 'LIST (user_device_type)'})

    uuid = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.users.uuid'), nullable=False)
    logged_in_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_agent = Column(Text)
    user_device_type = Column(Text, nullable=False, primary_key=True)

    user = relationship("User", back_populates="sign_ins")

    def __init__(self,
                 user_id: str,
                 logged_in_at: str,
                 user_agent: str,
                 user_device_type: str) -> None:
        self.user_id = user_id
        self.logged_in_at = logged_in_at
        self.user_agent = user_agent
        self.user_device_type = user_device_type

    def __repr__(self):
        return f'<UserSignIn {self.user_id}:{self.logged_in_at}>'
