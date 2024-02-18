from fastapi import APIRouter, Depends, HTTPException

from api.v1.models.users.answers.sign_up import SignUpAnswer, SignUpAnswerModel
from api.v1.models.users.results.user_response import UserResult
from services.user_service import UserService, get_user_service

router = APIRouter()


@router.post(
    path='/sign_up',
    response_model=SignUpAnswerModel,
    summary="Sign Up",
    description="Sign Up"
)
async def sign_up(
        login: str,
        password: str,
        first_name: str,
        last_name: str,
        service: UserService = Depends(get_user_service)
) -> SignUpAnswerModel:
    answer_type = await service.sign_up(
        login=login,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    answer = SignUpAnswer()
    results = answer.get_answer_model(answer_type)
    return results


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
