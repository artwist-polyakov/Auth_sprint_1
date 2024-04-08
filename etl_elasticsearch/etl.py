import logging
import time
from contextlib import contextmanager

import psycopg2
from configs.settings import PostgresSettings
from db.extractor_from_pg import PostgresExtractor
from db.loader_films_to_es import FilmsLoader
from db.loader_genres_to_es import GenresLoader
from db.loader_persons_to_es import PersonsLoader
from db.loader_to_es import ElasticLoader
from psycopg2.extras import DictCursor
from utils.mappers import (GenresPostgresDataMapper, PersonsPostgresDataMapper,
                           PostgresDataMapper)
from utils.redis_companion import RedisCompanion
from utils.utils import configure_logger

BATCH_SIZE = 100


# todo аннотция типов
class ETL:
    def __init__(self):
        self.redis = RedisCompanion()
        self.postgres_dsl = PostgresSettings().model_dump()
        self.counter = 0
        self.new_redis_keys = None

        self.fw = {
            "data": None,
            "mapper": PostgresDataMapper(),
            "loader": FilmsLoader(),
        }

        self.genres = {
            "data": None,
            "mapper": GenresPostgresDataMapper(),
            "loader": GenresLoader(),
        }

        self.persons = {
            "data": None,
            "mapper": PersonsPostgresDataMapper(),
            "loader": PersonsLoader(),
        }

        self.indexes = [self.fw, self.genres, self.persons]

    @contextmanager
    def pg_conn_context(self, **settings):
        conn = psycopg2.connect(**settings, cursor_factory=DictCursor)
        try:
            yield conn
        finally:
            conn.close()

    def extract(self, pg_conn):
        postgres_extractor = PostgresExtractor(pg_conn, BATCH_SIZE)
        data = postgres_extractor.extract_filmworks()
        self.new_redis_keys = data.new_keys_for_redis
        # внутри контейнера data также лежат
        # обновлённые ключи для Redis и person_data + genre_data
        self.fw["data"] = data.film_work_data
        if not self.fw["data"]:
            # если не пришло обновлений фильмов, то и другие сущности не обновлялись.
            logging.info("ETL no filmwork data to load — sleep 30 sec")
            time.sleep(30)
        self.genres["data"] = data.genre_data
        self.persons["data"] = data.person_data

    def transform(self, i, mapper):
        mapper.load_data(self.indexes[i]["data"])
        self.indexes[i]["data"] = mapper.get_for_es()

    def load(self, data, loader: ElasticLoader):
        loader.charge_data(data)
        loader.load_data()

    def etl(self):
        with self.pg_conn_context(**self.postgres_dsl) as pg_conn:
            configure_logger()
            while True:
                logging.info("ETL Start extracting data from Postgres")
                self.extract(pg_conn)

                logging.info("ETL Start transforming and loading")
                for i, index in enumerate(self.indexes):
                    self.transform(i, index["mapper"])
                    self.load(index["data"], index["loader"])

                logging.info("ETL Ended ETL iteration")

                for key, value in self.new_redis_keys.items():
                    self.redis.save_update_time(key, value)
                self.counter += 1
                if self.counter % 100 == 0:
                    logging.info(f"ETL counter: {self.counter}")

                time.sleep(0.5)


if __name__ == "__main__":
    etl = ETL()
    etl.etl()
