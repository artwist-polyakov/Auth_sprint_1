import datetime
import uuid
from dataclasses import dataclass, field


@dataclass
class PostgreFilmWork:
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime.date = field(default=datetime.date.today)
    file_path: str = field(default="")
    rating: float = field(default=0.0)
    type: str = field(default="movie")
    created: datetime.datetime = field(default=datetime.datetime.now)
    modified: datetime.datetime = field(default=datetime.datetime.now)


@dataclass
class PostgrePerson:
    id: uuid.UUID
    full_name: str
    created: datetime.datetime = field(default=datetime.datetime.now)
    modified: datetime.datetime = field(default=datetime.datetime.now)


@dataclass
class PostgreGenre:
    id: uuid.UUID
    name: str
    description: str
    created: datetime.datetime = field(default=datetime.datetime.now)
    modified: datetime.datetime = field(default=datetime.datetime.now)


@dataclass
class PostgreGenreFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created: datetime.datetime = field(default=datetime.datetime.now)


@dataclass
class PostgrePersonFilmWork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created: datetime.datetime = field(default=datetime.datetime.now)


# объявим датаклассы для передачи в ES
@dataclass
class FilmworkToTransform:
    """Класс конечных файлов, получаемых из таблицы Poastgres."""

    id: str = field(default="")
    title: str = field(default="")
    description: str = field(default="")
    rating: float = field(default=0.0)
    type: str = field(default="movie")
    created: datetime.datetime = field(default=datetime.datetime.now)
    modified: datetime.datetime = field(default=datetime.datetime.now)
    role: str = field(default="")
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_full_name: str = field(default="")
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_name: str = field(default="")
    genre_description: str = field(default="")


@dataclass
class GenreUpdate:
    id: str = field(default="")
    name: str = field(default="")
    description: str = field(default="")
    modified: datetime.datetime = field(default=datetime.datetime.now)


@dataclass
class PersonUpdate:
    id: str = field(default="")
    full_name: str = field(default="")
    modified: datetime.datetime = field(default=datetime.datetime.now)


@dataclass
class FilmWorkUpdate:
    id: str = field(default="")
    modified: datetime.datetime = field(default=datetime.datetime.now)


@dataclass
class BatchUpdate:
    """Класс для передачи данных из PostgresExtractor в загрузчик."""

    film_work_data: list[FilmworkToTransform] = field(default_factory=list)
    person_data: list[PersonUpdate] = field(default_factory=list)
    genre_data: list[GenreUpdate] = field(default_factory=list)
    new_keys_for_redis: dict[str, datetime] = field(default_factory=dict)
