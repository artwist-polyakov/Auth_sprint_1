from api.v1.models.output import Output


class WorkRecord(Output):
    uuid: str
    roles: list[str]
