from fastapi import APIRouter, Cookie, Depends
from fastapi.responses import JSONResponse, Response

from api.v1.models.users.results.user_result import UserResult
from api.v1.utils.api_convertor import APIConvertor
from db.models.token_models.access_token_container import AccessTokenContainer
from services.user_service import UserService, get_user_service
from utils.jwt_toolkit import dict_from_jwt, get_jwt_settings
from utils.wrappers import value_error_handler

router = APIRouter()


@router.get(
    path='/check',
    summary="Check access token",
    description="Check access token"
)
async def check_token(token: str) -> dict:
    return {'is_valid': 'login' in (dict_from_jwt(token).keys())}


@router.post(
    path='/sign_up',
    summary="Sign Up",
    description="Sign Up"
)
@value_error_handler()
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
    if response['status_code'] == 201:
        uuid = response['content']['uuid']
        # access_token = response['content']['access_token']
        refresh_token = response['content']['refresh_token']

        json_response = JSONResponse(
            status_code=response['status_code'],
            content={'uuid': uuid, "refresh_token": refresh_token, "token_type": 'bearer'}
        )

        # todo при создании пользователя мы пока не
        #  возвращаем токены в ответе (опционально добавим потом)

        # json_response.set_cookie(
        #     key="access_token",
        #     value=access_token,
        #     httponly=True
        # )
        # json_response.set_cookie(
        #     key="refresh_token",
        #     value=refresh_token,
        #     httponly=True,
        #     expires=10
        # )
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
    if not check_token(access_token):
        return JSONResponse(
            status_code=401,
            content='Invalid access token'
        )
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
    if not check_token(access_token):
        return JSONResponse(
            status_code=401,
            content='Invalid access token'
        )
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

    if isinstance(response, AccessTokenContainer):
        access = APIConvertor().map_token_container_to_access_token(response)
        refresh = APIConvertor().map_token_container_to_refresh_token(response)
        json_result = JSONResponse(
            status_code=200,
            content={"refresh_token": access,
                     "access_token": refresh,
                     "token_type": 'bearer'}
        )
        json_result.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            expires=get_jwt_settings().access_token_expire_minutes*60
        )

        json_result.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            expires=get_jwt_settings().refresh_token_expire_minutes*60
        )
        return json_result
    else:
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
        uuid: str,
        login: str,
        first_name: str,
        last_name: str,
        access_token: str = Cookie(None),
        service: UserService = Depends(get_user_service)
) -> Response:
    if not check_token(access_token):
        return JSONResponse(
            status_code=401,
            content='Invalid access token'
        )
    response: dict = await service.update_profile(uuid, login, first_name, last_name)
    return JSONResponse(
        status_code=response['status_code'],
        content=response['content']
    )
