from fastapi import APIRouter, Depends
from fastapi.responses import Response, JSONResponse

from api.v1.models.users.results.user_result import UserResult
from db.models.auth_responses.user_response import UserResponse
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
    response: dict = await service.sign_up(
        login=login,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    return JSONResponse(
        status_code=response['status_code'],
        content=response['content']
    )


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
    response: dict = await service.get_user_by_uuid(uuid)
    if response['status_code'] == 200:
        return UserResult(
            uuid=str(response['content']['uuid']),
            login=response['content']['login'],
            first_name=response['content']['first_name'],
            last_name=response['content']['last_name'],
            is_verified=response['content']['is_verified']
        )
    else:
        return JSONResponse(
                status_code=response['status_code'],
                content=response['content']
            )


@router.post(
    path='/delete',
    summary="Delete User by UUID",
    description="Delete one user with current uuid if exists"
)
async def delete_user(
        uuid: str,
        service: UserService = Depends(get_user_service)
) -> Response:
    response: dict = await service.remove_account(uuid)
    return JSONResponse(
        status_code=response['status_code'],
        content=response['content']
    )


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
    response: dict = await service.authenticate(login, password)
    return JSONResponse(
        status_code=response['status_code'],
        content=response['content']
    )


@router.post(
    path='/update',
    summary="Update Profile Data",
    description="Update profile data except password"
)
async def update_user(
        uuid: str,  # передается, чтобы можно было поменять логин
        login: str,
        first_name: str,
        last_name: str,
        service: UserService = Depends(get_user_service)
) -> Response:
    response: dict = await service.update_profile(uuid, login, first_name, last_name)
    return JSONResponse(
        status_code=response['status_code'],
        content=response['content']
    )
