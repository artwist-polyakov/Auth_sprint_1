from fastapi import APIRouter, Depends


from api.v1.models.users.sign_up import SignUpAnswer, SignUpAnswerModel
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
