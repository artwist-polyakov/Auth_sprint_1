from models.elastic_models import (DataclassForElastic, GenreDataForElastic,
                                   GenreElement, PersonDataForElastic,
                                   PersonIdName)
from models.postgres_models import (FilmworkToTransform, GenreUpdate,
                                    PersonUpdate)


class PostgresDataMapper:
    _data_storage: list[FilmworkToTransform] = []
    _data_set: dict[DataclassForElastic:DataclassForElastic] = {}

    def load_data(self, data: list[FilmworkToTransform]):
        self._data_storage = data
        self._data_set = {}
        self.transform_data()

    def transform_data(self):
        for item in self._data_storage:
            pkey = str(item.id)
            if str(pkey) not in self._data_set.keys():
                self._data_set[pkey] = self._map_dataclass(item)
            else:
                new_item = self._match_diferences(self._data_set[pkey], item)
                self._data_set[pkey] = new_item

    def _map_dataclass(self, dataclass: FilmworkToTransform) -> DataclassForElastic:
        return DataclassForElastic(
            id=str(dataclass.id),
            imdb_rating=dataclass.rating if dataclass.rating else 0.0,
            genres=[
                GenreElement(
                    id=str(dataclass.genre_id),
                    name=dataclass.genre_name,
                    description=dataclass.genre_description
                    if dataclass.genre_description
                    else "",
                )
            ],
            title=dataclass.title,
            description=dataclass.description,
            directors=[dataclass.person_full_name]
            if dataclass.role == "director"
            else [],
            actor_names=[dataclass.person_full_name]
            if dataclass.role == "actor"
            else [],
            writers_names=[dataclass.person_full_name]
            if dataclass.role == "writer"
            else [],
            actors=[
                PersonIdName(
                    person_id=str(dataclass.person_id), name=dataclass.person_full_name
                )
            ]
            if dataclass.role == "actor"
            else [],
            writers=[
                PersonIdName(
                    person_id=str(dataclass.person_id), name=dataclass.person_full_name
                )
            ]
            if dataclass.role == "writer"
            else [],
            directors_list=[
                PersonIdName(
                    person_id=str(dataclass.person_id), name=dataclass.person_full_name
                )
            ]
            if dataclass.role == "director"
            else [],
        )

    def _match_diferences(
        self, current: DataclassForElastic, new: FilmworkToTransform
    ) -> DataclassForElastic:
        # отличаться могут только жанры, актёры, режиссёры и сценаристы
        # причем если нашли одно отличие, то дальше можно не искать.
        if new.genre_id not in [genre.id for genre in current.genres]:
            current.genres.append(
                GenreElement(
                    id=str(new.genre_id),
                    name=new.genre_name,
                    description=new.genre_description if new.genre_description else "",
                )
            )
            return current

        if new.role == "actor":
            if (
                PersonIdName(person_id=str(new.person_id), name=new.person_full_name)
                not in current.actors
            ):
                current.actors.append(
                    PersonIdName(
                        person_id=str(new.person_id), name=new.person_full_name
                    )
                )
                current.actor_names.append(new.person_full_name)
                return current

        if new.role == "director":
            if (
                PersonIdName(person_id=str(new.person_id), name=new.person_full_name)
                not in current.directors_list
            ):
                current.directors_list.append(
                    PersonIdName(
                        person_id=str(new.person_id), name=new.person_full_name
                    )
                )
                current.directors.append(new.person_full_name)
                return current

        if new.role == "writer":
            if (
                PersonIdName(person_id=str(new.person_id), name=new.person_full_name)
                not in current.writers
            ):
                current.writers.append(
                    PersonIdName(
                        person_id=str(new.person_id), name=new.person_full_name
                    )
                )
                current.writers_names.append(new.person_full_name)
                return current

        return current

    def get_for_es(self) -> list[DataclassForElastic]:
        return list(self._data_set.values())


class GenresPostgresDataMapper:
    _data_storage: list[GenreUpdate] = []
    _data_set: dict[GenreDataForElastic:GenreDataForElastic] = {}

    def load_data(self, data: list[GenreUpdate]):
        self._data_storage = data
        self._data_set = {}
        self.transform_data()

    def transform_data(self):
        for item in self._data_storage:
            pkey = str(item.id)
            if str(pkey) not in self._data_set.keys():
                self._data_set[pkey] = self._map_dataclass(item)
            else:
                self._data_set[pkey] = item

    def _map_dataclass(self, dataclass: GenreUpdate) -> GenreDataForElastic:
        return GenreDataForElastic(
            id=str(dataclass.id), name=dataclass.name, description=dataclass.description
        )

    def get_for_es(self) -> list[DataclassForElastic]:
        return list(self._data_set.values())


class PersonsPostgresDataMapper:
    _data_storage: list[PersonUpdate] = []
    _data_set: dict[PersonDataForElastic:PersonDataForElastic] = {}

    def load_data(self, data: list[PersonUpdate]):
        self._data_storage = data
        self._data_set = {}
        self.transform_data()

    def transform_data(self):
        for item in self._data_storage:
            pkey = str(item.id)
            if str(pkey) not in self._data_set.keys():
                self._data_set[pkey] = self._map_dataclass(item)
            else:
                self._data_set[pkey] = item

    def _map_dataclass(self, dataclass: PersonUpdate) -> PersonDataForElastic:
        return PersonDataForElastic(id=str(dataclass.id), full_name=dataclass.full_name)

    def get_for_es(self) -> list[DataclassForElastic]:
        return list(self._data_set.values())
