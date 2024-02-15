from db.models.auth_responses.answer import Answer, BaseAnswerModel


class SignUpAnswer(Answer):
    def __init__(self, answer_type: bool):
        self.answer_type: bool = answer_type
        self.message: str = ''

    def get_answer_model(self):
        if self.answer_type:
            self.message = 'Пользователь успешно зарегистрирован'
        else:
            self.message = 'Регистрация не удалась'

        return SignUpAnswerModel(
            answer_type=self.answer_type,
            message=self.message
        )


class SignUpAnswerModel(BaseAnswerModel):
    answer_type: bool
    message: str

