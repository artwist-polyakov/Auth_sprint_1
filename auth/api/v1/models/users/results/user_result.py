from api.v1.models.output import Output


class UserResult(Output):
    uuid: str
    email: str
    first_name: str
    last_name: str
