from api.v1.models.users.answer import Answer
from db.models.auth_responses.auth_answers.signup_answers import SignUpAnswer


class UserConvertor:

    def map_sign_up(
            self,
            response_type: SignUpAnswer,
            params: dict = {}
    ) -> Answer:


