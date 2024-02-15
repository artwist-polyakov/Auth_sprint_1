from fastapi import APIRouter, Depends

from api.v1.models.users.answer import Answer
from api.v1.utils.user_convertor import UserConvertor
from db.postgres import PostgresProvider
from services.user_service import UserService

router = APIRouter()
convertor = UserConvertor()


def get_user_service():
    postgres = PostgresProvider()
    session = postgres.get_session()
    return UserService(session)


@router.post(
   path='/sign_up',
   response_model=Answer,
   summary="Sign Up",
   description="Sign Up"
)
async def sign_up(
        login: str, password: str, first_name: str, last_name: str,
        user_service: UserService = Depends(get_user_service),
) -> Answer:
    user_data = {'login': login, 'password': password,
                 'first_name': first_name, 'last_name': last_name}
    results = await user_service.sign_up(data=user_data)
    return convertor.map_sign_up(results)

