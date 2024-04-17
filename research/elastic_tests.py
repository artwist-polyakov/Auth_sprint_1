import time

from elasticsearch import Elasticsearch

# Подключение к Elasticsearch
els_con = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
index_name = "test_db"


def create_index(index_name: str):
    # Проверка наличия индекса
    if els_con.indices.exists(index=index_name):
        return

    mappings = {
        "properties": {
            "id": {"type": "keyword"},
            "value": {"type": "text", "analyzer": "russian"}
        },
        "dynamic_templates": [
            {
                "strings_as_text": {
                    "match_mapping_type": "string",
                    "mapping": {
                        "type": "text",
                        "analyzer": "russian"
                    }
                }
            }
        ]
    }

    settings = {
        "analysis": {
            "filter": {
                "russian_stop": {
                    "type":       "stop",
                    "stopwords":  "_russian_"
                },
                "russian_stemmer": {
                    "type":       "stemmer",
                    "language":   "russian"
                }
            },
            "analyzer": {
                "russian": {
                    "tokenizer": "standard",
                    "filter": ["lowercase", "russian_stop", "russian_stemmer"]
                }
            }
        }
    }

    # Создание индекса с указанными маппингами и настройками
    els_con.indices.create(index=index_name, body={"mappings": mappings, "settings": settings})


def load_data(data):
    # Вызов функции для проверки наличия или создания индекса
    create_index(index_name=index_name)
    # Запись
    start = time.monotonic()
    for record in data:
        els_con.index(index=index_name, body=record)
    end = time.monotonic()
    return end - start


def load_data(data):
    # Вызов функции для проверки наличия или создания индекса
    create_index(index_name=index_name)
    # Запись
    start = time.monotonic()
    for record in data:
        els_con.index(index=index_name, body=record)
    end = time.monotonic()
    return end - start

def read_data():
    # Поиск всех записей в индексе
    start = time.monotonic()
    result = els_con.search(index=index_name, body={"query": {"match_all": {}}})

    end = time.monotonic()
    return result['hits']['hits'], end - start
