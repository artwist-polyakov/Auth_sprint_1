from api.v1.models.output import Output


class Person(Output):
    uuid: str
    full_name: str
