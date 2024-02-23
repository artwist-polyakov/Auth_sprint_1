from api.v1.models.output import Output
from api.v1.models.persons.work_record import WorkRecord


class PersonFilms(Output):
    uuid: str
    full_name: str
    films: list[WorkRecord]
