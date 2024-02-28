from api.v1.models.output import Output


class DetailedGenre(Output):
    uuid: str
    name: str
    description: str = ''
