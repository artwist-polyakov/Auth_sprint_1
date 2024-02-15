from api.v1.models.output import Output


class Answer(Output):
    answer_type: str
    message: str
