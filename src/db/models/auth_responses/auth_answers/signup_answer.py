from db.models.auth_responses.answer import Answer, BaseAnswerModel


SIGNUP_ANSWER_TYPES = {
    'success': 'Пользователь успешно зарегистрирован',
    'fail': 'Регистрация не удалась'
}


class SignUpAnswer(Answer):
    def __init__(self, answer_type: str):
        self.answer_type: str = answer_type
        self.message: str = ''

    def get_answer_model(self):
        self.message = SIGNUP_ANSWER_TYPES[self.answer_type]
        return SignUpAnswerModel(
            message=self.message
        )


class SignUpAnswerModel(BaseAnswerModel):
    message: str

