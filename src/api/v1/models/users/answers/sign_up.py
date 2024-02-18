from api.v1.models.users.answers.answer import Answer, BaseAnswerModel

SIGNUP_ANSWER_TYPES = {
    '201_success': 'Пользователь успешно зарегистрирован',
    '409_already_exists': 'Пользователь с этим логином уже существует'
}


class SignUpAnswer(Answer):
    def __init__(self):
        super().__init__()
        self.answer_types = SIGNUP_ANSWER_TYPES
        self.answer_model = SignUpAnswerModel


class SignUpAnswerModel(BaseAnswerModel):
    message: str

