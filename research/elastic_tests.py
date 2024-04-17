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


def load_data(data, batch_size):
    create_index(index_name)  # Проверка наличия или создания индекса

    # Разбиваем данные на батчи
    batches = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

    # Запись данных батчами
    start = time.monotonic()
    for batch in batches:
        actions = []
        for record in batch:
            action = {
                "index": {
                    "_index": index_name,
                    "_id": record['id']  # Используем поле 'id' как идентификатор документа
                }
            }
            actions.append(action)
            actions.append(record)

        els_con.bulk(body=actions)
    end = time.monotonic()
    return end - start


def read_data():
    # Поиск всех записей в индексе
    start = time.monotonic()
    result = els_con.search(index=index_name, body={"query": {"match_all": {}}})
    # for item in read_result:
    #     print(item['_source'])
    end = time.monotonic()
    return result['hits']['hits'], end - start
