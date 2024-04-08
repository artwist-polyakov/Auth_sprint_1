from dataclasses import dataclass, field


@dataclass
class PersonIdName:
    person_id: str = field(default="")
    name: str = field(default="")


@dataclass
class GenreElement:
    id: str = field(default="")
    name: str = field(default="")
    description: str = field(default="")


@dataclass
class DataclassForElastic:
    id: str = field(default="")
    imdb_rating: float = field(default=0.0)
    genres: list[GenreElement] = field(default_factory=list)
    title: str = field(default="")
    description: str = field(default="")
    directors: list[str] = field(default_factory=list)
    actor_names: list[str] = field(default_factory=list)
    writers_names: list[str] = field(default_factory=list)
    actors: list[PersonIdName] = field(default_factory=list)
    writers: list[PersonIdName] = field(default_factory=list)
    directors_list: list[PersonIdName] = field(default_factory=list)


@dataclass
class GenreDataForElastic:
    id: str = field(default="")
    name: str = field(default="")
    description: str = field(default="")


@dataclass
class PersonDataForElastic:
    id: str = field(default="")
    full_name: str = field(default="")
