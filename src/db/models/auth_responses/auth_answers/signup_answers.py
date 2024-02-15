from db.models.auth_responses.answer import Answer


class SignUpAnswer(Answer):
    def __init__(self, answer_type: bool):
        self.answer_type: bool = answer_type
        self.message: str = ''

    def get_message(self):
        if self.answer_type:
            self.message = 'Пользователь успешно зарегистрирован'
        else:
            self.message = 'Регистрация не удалась'
        return self.message
