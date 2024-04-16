from elasticsearch import Elasticsearch
from uuid import uuid4

# Подключение к Elasticsearch
els_con = Elasticsearch([{'host': 'localhost', 'port': 9200}])
index_name = "test_db"


def create_index(index_name):
    # Проверка наличия индекса
    if els_con.indices.exists(index=index_name):
        print(f"Индекс {index_name} уже существует")
        return

    # Создание настроек (settings)
    settings = {
        "settings": {
            "refresh_interval": "1s",
            "analysis": {
                "filter": {
                    "english_stop": {
                        "type": "stop",
                        "stopwords": "_english_"
                    },
                    "english_stemmer": {
                        "type": "stemmer",
                        "language": "english"
                    },
                    "english_possessive_stemmer": {
                        "type": "stemmer",
                        "language": "possessive_english"
                    },
                    "russian_stop": {
                        "type": "stop",
                        "stopwords": "_russian_"
                    },
                    "russian_stemmer": {
                        "type": "stemmer",
                        "language": "russian"
                    }
                },
                "analyzer": {
                    "ru_en": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "english_stop",
                            "english_stemmer",
                            "english_possessive_stemmer",
                            "russian_stop",
                            "russian_stemmer"
                        ]
                    }
                }
            }
        }
    }

    # Создание маппинга
    mappings = {
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "value": {"type": "text", "analyzer": "ru_en"}
            }
        }
    }

    # Создание индекса с указанными маппингами и настройками
    els_con.indices.create(index=index_name, body={"settings": settings, "mappings": mappings})


def load_data(data):
    # Вызов функции для проверки наличия или создания индекса
    create_index(index_name)
    for record in data:
        els_con.index(index=index_name, body=record)


# Загрузка данных
data = [{"id": str(uuid4()), "value": "Example text 1"},
        {"id": str(uuid4()), "value": "Example text 2"}]

# Вызов функции для загрузки данных
load_data(data)
