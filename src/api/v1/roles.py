from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response

from services.role_service import RoleService, get_role_service

router = APIRouter()


@router.get(
    path='/roles',
    summary="Roles",
    description="Get all roles"
)
async def get_roles(
        service: RoleService = Depends(get_role_service)
) -> Response:
    response: dict = await service.get_roles()
    return JSONResponse(
        status_code=200,
        content=response
    )


@router.post(
    path='/add_role',
    summary="Add Role",
    description="Add role"
)
async def add_role(
        role: str,
        resource: str,
        verb: str,
        service: RoleService = Depends(get_role_service)
) -> Response:
    response = await service.add_role(role, resource, verb)
    return JSONResponse(
        status_code=200,
        content={'uuid': response}
    )


@router.put(
    path='/update_role',
    summary="Update Role",
    description="Update role"
)
async def update_role(
        uuid: str,
        role: str = '',
        resource: str = '',
        verb: str = '',
        service: RoleService = Depends(get_role_service)
) -> Response:
    response: dict = await service.update_role(uuid, role, resource, verb)
    return JSONResponse(
        status_code=response['status_code'],
        content=response['content']
    )
