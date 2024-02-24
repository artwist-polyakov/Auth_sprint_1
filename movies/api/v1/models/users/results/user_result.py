from api.v1.models.output import Output


class UserResult(Output):
    uuid: str
    login: str
    first_name: str
    last_name: str
