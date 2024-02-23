import logging

from fastapi import APIRouter, Cookie, Depends
from fastapi.responses import JSONResponse, Response

from api.v1.models.users.results.user_result import UserResult
from api.v1.utils.api_convertor import APIConvertor
from db.models.token_models.access_token_container import AccessTokenContainer
from services.user_service import UserService, get_user_service
from utils.jwt_toolkit import dict_from_jwt, get_jwt_settings
from utils.wrappers import value_error_handler

router = APIRouter()
USER_ID_KEY = 'user_id'
ROLE_KEY = 'role'
IS_SUPERUSER_KEY = 'is_superuser'
ADMIN_ROLE = 'admin'


def get_error_from_uuid(uuid: str, token: str | None) -> Response | None:
    if not token:
        return JSONResponse(
            status_code=401,
            content='Invalid access token'
        )
    decoded_uuid = dict_from_jwt(token).get(USER_ID_KEY, None)

    decoded_role = dict_from_jwt(token).get(ROLE_KEY, None)
    superuser = dict_from_jwt(token).get(IS_SUPERUSER_KEY, None)

    if superuser or decoded_role == ADMIN_ROLE:
        return None
    if not decoded_uuid or uuid != decoded_uuid:
        logging.warning(f"UUID: {uuid}, Decoded UUID: {decoded_uuid}")
        return JSONResponse(
            status_code=403,
            content="Your access token doesn't permit request to this user"
        )
    else:
        return None


def get_tokens_response(response: AccessTokenContainer | dict) -> Response:
    if isinstance(response, AccessTokenContainer):
        access = APIConvertor().map_token_container_to_access_token(response)
        refresh = APIConvertor().map_token_container_to_refresh_token(response)
        json_result = JSONResponse(
            status_code=200,
            content={"refresh_token": refresh,
                     "access_token": access,
                     "token_type": 'bearer'}
        )
        json_result.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            expires=get_jwt_settings().access_token_expire_minutes * 60
        )

        json_result.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            expires=get_jwt_settings().refresh_token_expire_minutes * 60
        )
        return json_result
    else:
        return JSONResponse(
            status_code=response['status_code'],
            content=response['content']
        )


@router.post(
    path='/sign_up',
    summary="Sign Up",
    description="Sign Up"
)
@value_error_handler()
async def sign_up(
        login: str,
        password: str,
        first_name: str = '',
        last_name: str = '',
        service: UserService = Depends(get_user_service)
) -> Response:
    response: dict = await service.sign_up(
        login=login,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    if response['status_code'] == 201:
        uuid = response['content']['uuid']

        json_response = JSONResponse(
            status_code=response['status_code'],
            content={'uuid': uuid, "token_type": 'cookie-jwt'}
        )

        return json_response
    else:
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
        access_token: str = Cookie(None),
        service: UserService = Depends(get_user_service)
) -> UserResult | Response:
    if error := get_error_from_uuid(uuid, access_token):
        return error
    response: dict = await service.get_user_by_uuid(uuid)
    if response['status_code'] == 200:
        return UserResult(
            uuid=str(response['content']['uuid']),
            login=response['content']['login'],
            first_name=response['content']['first_name'],
            last_name=response['content']['last_name']
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
        access_token: str = Cookie(None),
        service: UserService = Depends(get_user_service)
) -> Response:
    if error := get_error_from_uuid(uuid, access_token):
        return error
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
    return get_tokens_response(response)


@router.post(
    path='/update',
    summary="Update Profile Data",
    description="Update profile data except password"
)
async def update_user(
        uuid: str,
        login: str,
        first_name: str = '',
        last_name: str = '',
        access_token: str = Cookie(None),
        service: UserService = Depends(get_user_service)
) -> Response:
    if error := get_error_from_uuid(uuid, access_token):
        return error
    response: dict = await service.update_profile(uuid, login, first_name, last_name)
    return JSONResponse(
        status_code=response['status_code'],
        content=response['content']
    )


@router.post(
    path='/refresh',
    summary="Refresh access token via refresh token",
    description="Emits new access token if refresh token is valid"
)
async def refresh_access_token(
        refresh_token: str = Cookie(None),
        service: UserService = Depends(get_user_service)
) -> Response:
    if refresh_token is None:
        return JSONResponse(
            status_code=401,
            content='Invalid refresh token'
        )

    response: dict = await service.refresh_access_token(
        *APIConvertor.refresh_token_to_tuple(
            refresh_token
        )
    )
    return get_tokens_response(response) if response else JSONResponse(
        status_code=401,
        content='Invalid refresh token'
    )


@router.post(
    path='/logout',
    summary="Logout from current session",
    description="Terminate all sessions correspondend with current refresh token"
)
async def logout(
        access_token: str = Cookie(None),
        service: UserService = Depends(get_user_service)
) -> Response:
    token = AccessTokenContainer(
        **dict_from_jwt(access_token)
    )
    response: dict = await service.logout_session(
        token
    )

    return JSONResponse(
        status_code=response['status_code'],
        content=response['content']
    )

@router.post(
    path="/logout_all_devices",
    summary="Logout from all devices",
    description="Terminate all sessions correspondend with current user_id"
)
async def logout_all_devices(
        access_token: str = Cookie(None),
        service: UserService = Depends(get_user_service)
) -> Response:
    token = AccessTokenContainer(
        **dict_from_jwt(access_token)
    )
    response: dict = await service.logout_all_sessions(token)
    return JSONResponse(
        status_code=response['status_code'],
        content=response['content']
    )