from configs.settings import settings
from db.auth.user import Base


class UserUpdateRequest(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': f'{settings.postgres_schema_2}'}

    def __init__(self,
                 uuid: str,
                 login: str,
                 first_name: str,
                 last_name: str) -> None:
        self.uuid = uuid
        self.login = login
        self.first_name = first_name
        self.last_name = last_name
