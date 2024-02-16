from api.v1.models.users.answers.answer import Answer, BaseAnswerModel
from api.v1.models.users.answers.errors_answers import ERRORS_TYPES

SIGNUP_ANSWER_TYPES = {
    'Success': 'Пользователь успешно зарегистрирован',
    'IntegrityError': 'Пользователь с этим логином уже существует',
}


class SignUpAnswer(Answer):
    def __init__(self):
        self.message: str = ''

    def get_answer_model(self, answer_type: str):
        if answer_type in SIGNUP_ANSWER_TYPES:
            self.message = SIGNUP_ANSWER_TYPES[answer_type]

        elif answer_type in ERRORS_TYPES:
            self.message = ERRORS_TYPES[answer_type]

        else:
            self.message = ''

        return SignUpAnswerModel(
            message=self.message
        )


class SignUpAnswerModel(BaseAnswerModel):
    message: str

