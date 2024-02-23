import uuid
from datetime import datetime, timedelta
from functools import lru_cache

import bcrypt
from pydantic import BaseModel

from configs.settings import settings
from db.models.auth_requests.role_request import RoleRequest
from db.models.token_models.access_token_container import AccessTokenContainer
from db.models.token_models.refresh_token import RefreshToken
from db.postgres import PostgresProvider


class RoleService:
    def __init__(self, instance: PostgresProvider):
        self._postgres = instance

    async def get_roles(self) -> dict:
        roles: dict = await self._postgres.get_roles()
        return roles

    async def add_role(
            self,
            role: str,
            resource: str,
            verb: str
    ) -> None:
        request = RoleRequest(
            role=role,
            resource=resource,
            verb=verb
        )
        await self._postgres.add_single_data(request, 'role')
        return None


@lru_cache
def get_role_service():
    postgres = PostgresProvider()
    return RoleService(postgres)
