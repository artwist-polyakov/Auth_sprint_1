from configs.settings import settings
from db.auth.user import Base


class UserRequest(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': f'{settings.postgres_schema_2}'}

    def __init__(self,
                 uuid: str,
                 login: str,
                 password: str,
                 first_name: str,
                 last_name: str,
                 is_verified: bool) -> None:
        self.uuid = uuid
        self.login = login
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_verified = is_verified
