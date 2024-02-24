from configs.settings import ElasticSettings
from elasticsearch import AsyncElasticsearch


class ElasticProvider(object):
    _instance = None
    _es_instance: AsyncElasticsearch | None = None
    _settings = ElasticSettings()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls._instance = super(ElasticProvider, cls).__new__(cls)
        return cls._instance

    def __del__(self):
        if self._es_instance is not None:
            self._es_instance.close()

    async def get_elastic(self) -> AsyncElasticsearch:
        if self._es_instance is None:
            elastic_dsl = self._settings.model_dump()
            self._es_instance = AsyncElasticsearch(**elastic_dsl)
        return self._es_instance

    async def close(self):
        if self._es_instance is not None:
            await self._es_instance.close()
