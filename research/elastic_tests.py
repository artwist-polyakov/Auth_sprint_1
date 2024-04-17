import time

from elasticsearch import Elasticsearch

# Подключение к Elasticsearch
els_con = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
index_name = "test_db"

def create_index(index_name):
    # Проверка наличия индекса
    if els_con.indices.exists(index=index_name):
        print(f"Индекс {index_name} уже существует")
        return

    # Создание настроек (settings) и маппинга (mappings)
    settings = {
        "settings": {
            "analysis": {
                "filter": {
                    "ru_stop": {
                        "type": "stop",
                        "stopwords": "_russian_"
                    },
                    "ru_stemmer": {
                        "type": "stemmer",
                        "language": "russian"
                    },
                    "en_stop": {
                        "type": "stop",
                        "stopwords": "_english_"
                    },
                    "en_stemmer": {
                        "type": "stemmer",
                        "language": "english"
                    }
                },
                "analyzer": {
                    "custom_analyzer": {
                        "tokenizer": "standard",
                        "filter": ["lowercase", "ru_stop", "ru_stemmer", "en_stop", "en_stemmer"]
                    }
                }
            }
        }
    }

    mappings = {
        "properties": {
            "id": {"type": "keyword"},
            "value": {"type": "text", "analyzer": "custom_analyzer"}
        }
    }

    # Создание индекса с указанными маппингами и настройками
    els_con.indices.create(index=index_name, body={"settings": settings, "mappings": {"properties": mappings}})


def load_data(data):
    # Вызов функции для проверки наличия или создания индекса
    create_index(index_name)
    # Запись
    start = time.monotonic()
    for record in data:
        els_con.index(index=index_name, body=record)
    end = time.monotonic()
    return end - start
