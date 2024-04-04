import sqlite3
from contextlib import contextmanager
from dataclasses import astuple, fields

import psycopg2
from models.postgres_models import (PostgreFilmWork, PostgreGenre,
                                    PostgreGenreFilmWork, PostgrePerson,
                                    PostgrePersonFilmWork)
from psycopg2.extensions import cursor
from psycopg2.extras import DictCursor
from utils.utils import configure_logger

from core import config


class PGClient:
    def __init__(self):
        self.dsl = config.DSL

    @contextmanager
    def conn_context_postgres(self):
        conn = psycopg2.connect(**self.dsl, cursor_factory=DictCursor)
        try:
            yield conn
        finally:
            conn.close()


@contextmanager
def conn_context_sqlite():
    db_path = config.SQLITE_PATH
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


TABLE_NAMES_AND_DATACLASSES = {
    "film_work": PostgreFilmWork,
    "genre": PostgreGenre,
    "person": PostgrePerson,
    "genre_film_work": PostgreGenreFilmWork,
    "person_film_work": PostgrePersonFilmWork,
}


class LoaderToPostgres:
    batch_size = 500

    def __init__(self):
        self.schema_name = "content"
        self.pg_client = PGClient()
        self.sqlite_rows = []
        self.table_objects = []

    def extract_sqlite_data(self, curs: sqlite3.Cursor):
        rows = curs.fetchmany(self.batch_size)
        # Remove last Nones otherwise astuple() will raise TypeError
        self.sqlite_rows = [row for row in rows if row is not None]

    def transform_data_into_objects(self, table_name: str):
        table_class = TABLE_NAMES_AND_DATACLASSES[table_name]
        for i, row in enumerate(self.sqlite_rows):
            self.table_objects.append(table_class(*row))

    def save_data_to_pg(self, curs: cursor, table_name: str):
        table_class = TABLE_NAMES_AND_DATACLASSES[table_name]
        column_names = [field.name for field in fields(table_class)]

        column_names_str = ", ".join(column_names)
        col_count = ", ".join(["%s"] * len(column_names))  # '%s, %s
        bind_values = ",".join(
            curs.mogrify(f"({col_count})", astuple(table_object)).decode("utf-8")
            for table_object in self.table_objects
        )

        query = (
            f"INSERT INTO {self.schema_name}.{table_name} ({column_names_str}) "
            f"VALUES {bind_values}"
            f" ON CONFLICT (id) DO NOTHING"
        )
        curs.execute(query)

    def etl_to_postgres(self):
        with (
            conn_context_sqlite() as sqlite_conn,
            self.pg_client.conn_context_postgres() as pg_conn,
        ):
            # Открыть curses
            sqlite_curs = sqlite_conn.cursor()
            pg_curs = pg_conn.cursor()

            for table_name in TABLE_NAMES_AND_DATACLASSES.keys():
                sqlite_curs.execute(f"SELECT * FROM {table_name};")
                while True:
                    # Extract sqlite data
                    self.extract_sqlite_data(sqlite_curs)
                    if not self.sqlite_rows:
                        break

                    # Transform data into objects
                    self.transform_data_into_objects(table_name)

                    # Save postgres data
                    self.save_data_to_pg(pg_curs, table_name)
                    pg_conn.commit()

                    self.sqlite_rows = []
                    self.table_objects = []

            # Закрыть curses
            sqlite_curs.close()
            pg_curs.close()


if __name__ == "__main__":
    configure_logger()
    loader = LoaderToPostgres()
    loader.etl_to_postgres()
