from fastapi import APIRouter, Depends
from fastapi.responses import Response

from api.v1.models.users.results.user_response import UserResult
from services.user_service import UserService, get_user_service

router = APIRouter()


@router.post(
    path='/sign_up',
    summary="Sign Up",
    description="Sign Up"
)
async def sign_up(
        login: str,
        password: str,
        first_name: str,
        last_name: str,
        service: UserService = Depends(get_user_service)
) -> Response:
    response: Response = await service.sign_up(
        login=login,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    return response


@router.get(
    path='/user',
    response_model=UserResult,
    summary="Get User by UUID",
    description="Get one user with current uuid if exists"
)
async def get_user_by_uuid(
        uuid: str,
        service: UserService = Depends(get_user_service)
) -> UserResult | Response:
    result: dict | Response = await service.get_user_by_uuid(uuid)
    if isinstance(result, dict):
        return UserResult(**result)
    else:
        return result


@router.post(
    path='/delete',
    summary="Delete User by UUID",
    description="Delete one user with current uuid if exists"
)
async def delete_user(
        uuid: str,
        service: UserService = Depends(get_user_service)
) -> Response:
    response: Response = await service.remove_account(uuid)
    return response


@router.get(
    path='/login',
    summary="Login",
    description="Login by login and password"
)
async def login_user(
        login: str,
        password: str,
        service: UserService = Depends(get_user_service)
) -> Response:
    response: Response = await service.authenticate(login, password)
    return response
