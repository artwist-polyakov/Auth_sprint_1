import logging

from configs.test_settings import settings
from elasticsearch import Elasticsearch
from utils.wrappers import backoff, ping_service

logging.getLogger('elastic_transport').setLevel(logging.ERROR)


@backoff()
def get_es_client(host, port) -> Elasticsearch:
    es = Elasticsearch(
        hosts=[f"http://{host}:{port}"],
        verify_certs=False
    )
    return es


@backoff()
def main():
    es_client_1 = get_es_client(settings.es_1_host, settings.elastic_port)
    es_client_2 = get_es_client(settings.es_2_host, settings.elastic_port)
    ping_service(es_client_1, "Elasticsearch-1")
    ping_service(es_client_2, "Elasticsearch-2")


if __name__ == '__main__':
    main()
