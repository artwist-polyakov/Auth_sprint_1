from fastapi import APIRouter, Depends

from db.models.auth_responses.auth_answers.signup_answers import SignUpAnswerModel
from db.postgres import PostgresProvider
from services.user_service import UserService

router = APIRouter()


def get_user_service():
    postgres = PostgresProvider()
    session = postgres.get_session()
    return UserService(session)


service: UserService = get_user_service()


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
        last_name: str
) -> SignUpAnswerModel:
    results = await service.sign_up(
        login=login,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    return results
