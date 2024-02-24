from db.auth.user_storage import UserStorage
from db.creator import Creator
from db.logout.logout_storage import LogoutStorage


class StoragesCreator(Creator):
    """
    класс, который следит, чтобы был только один экземпляр класса и ничего больше.

    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(StoragesCreator, cls).__new__(cls)
        return cls._instance

    def __init__(
            self,
            logout_provider: LogoutStorage,
            users_provider: UserStorage):
        self._logout = logout_provider
        self._users = users_provider

    def get_logout_storage(self) -> LogoutStorage:
        return self._logout

    def get_users_storage(self) -> UserStorage:
        return self._users
