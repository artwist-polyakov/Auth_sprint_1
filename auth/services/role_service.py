import uuid
from functools import lru_cache

from db.models.auth_requests.role_request import RoleRequest
from db.postgres import PostgresInterface


class RoleService:
    def __init__(self, instance: PostgresInterface):
        self._postgres = instance

    async def get_roles(self) -> dict:
        roles: dict = await self._postgres.get_roles()
        return roles

    async def add_role(
            self,
            role: str,
            resource: str,
            verb: str
    ) -> str:
        request = RoleRequest(
            uuid=uuid.uuid4(),
            role=role,
            resource=resource,
            verb=verb
        )
        await self._postgres.add_single_data(request, 'role')
        return request.uuid

    async def update_role(
            self,
            uuid: str,
            role: str = '',
            resource: str = '',
            verb: str = ''
    ) -> dict:
        role_item = await self._postgres.get_single_role(uuid)

        if isinstance(role_item, dict):
            return {
                'status_code': 404,
                'content': 'Role not found'
            }

        if not role:
            role = role_item.role
        if not resource:
            resource = role_item.resource
        if not verb:
            verb = role_item.verb

        request = RoleRequest(
            uuid=uuid,
            role=role,
            resource=resource,
            verb=verb
        )
        response: dict = await self._postgres.update_role(request)
        return response

    async def remove_role(self, uuid: str) -> dict:
        response: dict = await self._postgres.delete_single_data(uuid, 'role')
        return response

    async def change_user_role(
            self,
            uuid: str,
            new_role: str
    ) -> dict:
        role_item = await self._postgres.get_single_user(
            field_name='uuid', field_value=uuid)

        if isinstance(role_item, dict):
            return {
                'status_code': 404,
                'content': 'User not found'
            }

        response: dict = await self._postgres.update_user_role(uuid, new_role)
        return response


@lru_cache
def get_role_service():
    postgres = PostgresInterface()
    return RoleService(postgres)
