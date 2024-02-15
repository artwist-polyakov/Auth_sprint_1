from configs.settings import settings
from db.auth.user import Base


class UserRequest(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': f'{settings.postgres_schema_2}'}

    def __init__(self, login: str, password: str, first_name: str, last_name: str) -> None:
        self.login = login
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
