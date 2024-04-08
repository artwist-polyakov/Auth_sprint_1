from configs.elastic_shemas_config import GENRES_INDEX_SCHEMA
from db.loader_to_es import ElasticLoader
from models.elastic_models import GenreDataForElastic


class GenresLoader(ElasticLoader):
    _index_name: str = "genres"
    _schema: dict = GENRES_INDEX_SCHEMA
    _dataclass = GenreDataForElastic

    def _map_dataclass(self, dataclass: _dataclass) -> dict:
        return {
            "id": str(dataclass.id),
            "name": dataclass.name,
            "description": dataclass.description,
        }
