import time

from configs.test_settings import logger, settings
from elastic_shemas_config import (GENRES_INDEX_SCHEMA, MOVIES_INDEX_SCHEMA,
                                   PERSONS_INDEX_SCHEMA)
from elasticsearch import Elasticsearch


def create_index(es_client, index_name, schema):
    try:
        logger.info(f'Cоздание индекса {index_name}...')
        if es_client.indices.exists(index=index_name):
            es_client.indices.delete(index=index_name)

        es_client.indices.create(index=index_name, body=schema)
        logger.info(f'Индекс {index_name} создан')
    except Exception as e:
        logger.warning(f"Ошибка подключения к Elasticsearch: {e}")
        logger.warning("Повторная попытка подключения через 5 секунд...")
        time.sleep(5)
        create_index(es_client, index_name, schema)


if __name__ == '__main__':
    logger.info('Создаю индексы...')

    es_client = Elasticsearch(
        hosts=[f"http://{settings.es_1_host}:{settings.elastic_port}"],
        verify_certs=False
    )

    names_schemas = {'movies': MOVIES_INDEX_SCHEMA,
                     'persons': PERSONS_INDEX_SCHEMA,
                     'genres': GENRES_INDEX_SCHEMA}

    for index_name, schema in names_schemas.items():
        create_index(es_client, index_name, schema)

    logger.info('Закончил создавать индексы')
