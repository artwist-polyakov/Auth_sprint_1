from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

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
) -> JSONResponse:
    response = await service.sign_up(
        login=login,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    if response.status_code == 201:
        return JSONResponse(content={"message": "Пользователь успешно зарегистрирован"},
                            status_code=status.HTTP_201_CREATED)
    elif response.status_code == 409:
        raise HTTPException(status_code=409, detail="Пользователь с этим логином уже существует")
    else:
        raise HTTPException(status_code=500, detail="Попробуйте позже")


@router.get(
    path='/user',
    response_model=UserResult,
    summary="Get User by UUID",
    description="Get one user with current uuid if exists"
)
async def get_user_by_uuid(
        uuid: str,
        service: UserService = Depends(get_user_service)
) -> UserResult:
    result: dict = await service.get_user_by_uuid(uuid)
    if result:
        return UserResult(**result)
    else:
        raise HTTPException(status_code=404, detail="Пользователь не найден")


@router.post(
    path='/delete',
    summary="Delete User by UUID",
    description="Delete one user with current uuid if exists"
)
async def delete_user(
        uuid: str,
        service: UserService = Depends(get_user_service)
) -> JSONResponse:
    response = await service.remove_account(uuid)
    if response.status_code == 200:
        return JSONResponse(content={"message": "Пользователь успешно удален"},
                            status_code=status.HTTP_200_OK)
    if response.status_code == 404:
        return JSONResponse(content={"message": "Пользователь не найден"},
                            status_code=status.HTTP_404_NOT_FOUND)
    else:
        raise HTTPException(status_code=500, detail="Попробуйте позже")
