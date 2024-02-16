from db.models.auth_responses.answer import Answer, BaseAnswerModel
from db.models.auth_responses.auth_answers.exception_answers import ERRORS_TYPES

SIGNUP_ANSWER_TYPES = {
    'success': 'Пользователь успешно зарегистрирован',
    'IntegrityError': 'Пользователь с этим логином уже существует',
}


class SignUpAnswer(Answer):
    def __init__(self, answer_type: str):
        self.answer_type: str = answer_type  # передается из PostgresProvider
        self.message: str = ''

    def get_answer_model(self):
        if self.answer_type in SIGNUP_ANSWER_TYPES:
            self.message = SIGNUP_ANSWER_TYPES[self.answer_type]
        else:
            self.message = ERRORS_TYPES[self.answer_type]
        return SignUpAnswerModel(
            message=self.message
        )


class SignUpAnswerModel(BaseAnswerModel):
    message: str

