from api.v1.models.output import Output


class Answer:
    def __init__(self):
        self.answer_types: dict
        self.answer_model: BaseAnswerModel

    def get_answer_model(self, answer_type: str):
        if answer_type in self.answer_types:
            message = self.answer_types[answer_type]
        else:
            message = ''
        return self.answer_model(message=message)


class BaseAnswerModel(Output):
    pass
