from api.v1.models.output import Output


class FilmBrief(Output):
    uuid: str
    title: str
    imdb_rating: float
