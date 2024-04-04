import datetime
import uuid
from dataclasses import dataclass, field

from etl.models.postgres_models import (PostgreFilmWork, PostgreGenre,
                                        PostgreGenreFilmWork, PostgrePerson,
                                        PostgrePersonFilmWork)


@dataclass
class SQLLiteDatabaseMixin:
    id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    created_at: datetime.datetime = field(default=datetime.datetime.now, init=False)
    updated_at: datetime.datetime = field(default=datetime.datetime.now, init=False)


@dataclass
class FilmWork(SQLLiteDatabaseMixin):
    """Имеет метод map_to_postgre,.

    который возвращает объект подходящий схеме данных PostgreFilmWork
    """

    title: str
    description: str = field(default="")
    creation_date: datetime.date = field(default=datetime.date.today)
    file_path: str = field(default="")
    rating: float = field(default=0.0)
    type: str = field(default="movie")

    def map_to_postgre(self):
        new_description = self.description if self.description is not None else ""
        return PostgreFilmWork(
            title=self.title,
            description=new_description,
            id=self.id,
            creation_date=self.created_at,
            rating=self.rating if self.rating is not None else 0.0,
            type=self.type,
            created=self.created_at,
            modified=self.updated_at,
        )


@dataclass
class Person(SQLLiteDatabaseMixin):
    """Имеет метод map_to_postgre,.

    который возвращает объект подходящий схеме данных PostgreFilmWork
    """

    full_name: str

    def map_to_postgre(self):
        return PostgrePerson(
            full_name=self.full_name,
            id=self.id,
            created=self.created_at,
            modified=self.updated_at,
        )


@dataclass
class Genre(SQLLiteDatabaseMixin):
    """Имеет метод map_to_postgre,.

    который возвращает объект подходящий схеме данных PostgreFilmWork
    """

    name: str
    description: str

    def map_to_postgre(self):
        new_description = self.description if self.description is not None else ""
        return PostgreGenre(
            name=self.name,
            description=new_description,
            id=self.id,
            created=self.created_at,
            modified=self.updated_at,
        )


@dataclass
class GenreFilmWork:
    """Имеет метод map_to_postgre,.

    который возвращает объект подходящий схеме данных PostgreFilmWork
    """

    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime.datetime = field(default=datetime.datetime.now)

    def map_to_postgre(self):
        return PostgreGenreFilmWork(
            film_work_id=self.film_work_id,
            genre_id=self.genre_id,
            id=self.id,
            created=self.created_at,
        )


@dataclass
class PersonFilmWork:
    """Имеет метод map_to_postgre,.

    который возвращает объект подходящий схеме данных PostgreFilmWork
    """

    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime.datetime = field(default=datetime.datetime.now)

    def map_to_postgre(self):
        return PostgrePersonFilmWork(
            film_work_id=self.film_work_id,
            person_id=self.person_id,
            role=self.role,
            id=self.id,
            created=self.created_at,
        )
