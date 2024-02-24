from api.v1.models.output import Output


class Person(Output):
    """Модель ответа API для персоны"""
    uuid: str
    full_name: str
