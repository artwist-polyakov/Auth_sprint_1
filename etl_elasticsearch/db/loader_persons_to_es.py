from configs.elastic_shemas_config import PERSONS_INDEX_SCHEMA
from db.loader_to_es import ElasticLoader
from models.elastic_models import PersonDataForElastic


class PersonsLoader(ElasticLoader):
    _index_name: str = "persons"
    _schema: dict = PERSONS_INDEX_SCHEMA
    _dataclass = PersonDataForElastic

    def _map_dataclass(self, dataclass: _dataclass) -> dict:
        return {"id": str(dataclass.id), "full_name": dataclass.full_name}
