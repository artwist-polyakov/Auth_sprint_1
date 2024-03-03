import logging
from http import HTTPStatus

from api.v1.models.auth_schema import AuthSchema, UpdateSchema
from api.v1.models.paginated_params import PaginatedParams
from api.v1.models.users.results.user_result import UserResult
from api.v1.utils.api_convertor import APIConvertor
from configs.devices import devices
from db.models.token_models.access_token_container import AccessTokenContainer
from fastapi import APIRouter, Cookie, Depends
from fastapi.responses import JSONResponse, Response
from services.models.permissions import RBACInfo
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
            status_code=HTTPStatus.UNAUTHORIZED,
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
            status_code=HTTPStatus.FORBIDDEN,
            content="Your access token doesn't permit request to this user"
        )
    return None


def get_tokens_response(response: AccessTokenContainer | dict) -> Response:
    if isinstance(response, AccessTokenContainer):
        access = APIConvertor().map_token_container_to_access_token(response)
        refresh = APIConvertor().map_token_container_to_refresh_token(response)
        json_result = JSONResponse(
            status_code=HTTPStatus.OK,
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
    return JSONResponse(
        status_code=response['status_code'],
        content=response['content']
    )

# todo ^unauthorised
@router.post(
    path='/sign_up',
    summary="Sign Up",
    description="Sign Up"
)
@value_error_handler()
async def sign_up(
        auth_data: AuthSchema = Depends(),
        service: UserService = Depends(get_user_service)
) -> Response:
    response: dict = await service.sign_up(
        email=auth_data.email,
        password=auth_data.password,
        first_name=auth_data.first_name,
        last_name=auth_data.last_name
    )
    if response['status_code'] == HTTPStatus.CREATED:
        uuid = response['content']['uuid']

        json_response = JSONResponse(
            status_code=response['status_code'],
            content={'uuid': uuid, "token_type": 'cookie-jwt'}
        )

        return json_response
    return JSONResponse(
        status_code=response['status_code'],
        content=response['content']
    )

# todo ^user, admin
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
    if response['status_code'] == HTTPStatus.OK:
        return UserResult(
            uuid=str(response['content']['uuid']),
            email=response['content']['email'],
            first_name=response['content']['first_name'],
            last_name=response['content']['last_name']
        )
    return JSONResponse(
        status_code=response['status_code'],
        content=response['content']
    )

# todo ^user, admin
@router.delete(
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

# todo ^unauthorised
@router.get(
    path='/login',
    summary="Login",
    description=f"Login by email and password. List of available devices types: {devices}"
)
async def login_user(
        email: str,
        password: str,
        user_device_type: str,
        service: UserService = Depends(get_user_service)
) -> Response:
    if user_device_type not in devices:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content='No such device type'
        )
    response: dict = await service.authenticate(email, password, user_device_type)
    return get_tokens_response(response)

# todo ^user, admin
@router.patch(
    path='/update',
    summary="Update Profile Data",
    description="Update profile data except password"
)
async def update_user(
        uuid: str,
        update_data: UpdateSchema = Depends(),
        access_token: str = Cookie(None),
        service: UserService = Depends(get_user_service)
) -> Response:
    if error := get_error_from_uuid(uuid, access_token):
        return error
    response: dict = await service.update_profile(
        uuid,
        update_data.email,
        update_data.first_name,
        update_data.last_name
    )
    return JSONResponse(
        status_code=response['status_code'],
        content=response['content']
    )

# todo ^user
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
            status_code=HTTPStatus.UNAUTHORIZED,
            content='Invalid refresh token'
        )

    response: dict = await service.refresh_access_token(
        *APIConvertor.refresh_token_to_tuple(
            refresh_token
        )
    )
    return get_tokens_response(response) if response else JSONResponse(
        status_code=HTTPStatus.UNAUTHORIZED,
        content='Invalid refresh token'
    )

# todo ^user
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

# todo ^user
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

# todo ^user, admin
@router.get(
    path="/history",
    summary="Get login history",
    description="Get login history for current user"
)
async def get_login_history(
        pagination: PaginatedParams = Depends(),
        access_token: str = Cookie(None),
        service: UserService = Depends(get_user_service)
) -> Response:
    if not access_token:
        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content='Invalid access token'
        )
    token = AccessTokenContainer(
        **dict_from_jwt(access_token)
    )
    response: dict = await service.get_login_history(
        user_id=token.user_id,
        page=pagination.page,
        size=pagination.size
    )
    result = {
        'page': pagination.page,
        'pages': response['total'] // pagination.size + 1,
        'per_page': pagination.size,
        'total': response['total'],
        'results': response['history']
    }
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=result
    )

# todo ^admin
@router.get(
    path="/check_permissions",
    summary="Check permissions",
    description="Check permissions for current user"
)
async def check_permissions(
        resource: str,
        verb: str,
        access_token: str = Cookie(None),
        service: UserService = Depends(get_user_service)
) -> Response:
    if not access_token:
        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content='Invalid access token'
        )
    token = AccessTokenContainer(
        **dict_from_jwt(access_token)
    )
    rbac = RBACInfo(
        role=token.role,
        resource=resource,
        verb=verb
    )
    response: bool = await service.check_permissions(token, rbac)
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=response
    )
