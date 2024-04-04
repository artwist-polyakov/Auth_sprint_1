from configs.elastic_shemas_config import MOVIES_INDEX_SCHEMA
from db.loader_to_es import ElasticLoader
from models.elastic_models import (DataclassForElastic, GenreElement,
                                   PersonIdName)


class FilmsLoader(ElasticLoader):
    _index_name: str = "movies"
    _schema: dict = MOVIES_INDEX_SCHEMA
    _dataclass = DataclassForElastic

    def _map_dataclass(self, dataclass: DataclassForElastic) -> dict:
        return {
            "id": str(dataclass.id),
            "imdb_rating": float(dataclass.imdb_rating),
            "genres": [self._genre_to_dict(genre) for genre in dataclass.genres],
            "title": dataclass.title,
            "description": dataclass.description,
            "directors_names": dataclass.directors,
            "actors_names": dataclass.actor_names,
            "writers_names": dataclass.writers_names,
            "actors": [self._id_name_to_dict(actor) for actor in dataclass.actors],
            "writers": [self._id_name_to_dict(writer) for writer in dataclass.writers],
            "directors": [
                self._id_name_to_dict(director) for director in dataclass.directors_list
            ],
        }

    @staticmethod
    def _id_name_to_dict(data: PersonIdName):
        return {"id": str(data.person_id), "name": data.name}

    @staticmethod
    def _genre_to_dict(data: GenreElement):
        return {"id": str(data.id), "name": data.name, "description": data.description}
