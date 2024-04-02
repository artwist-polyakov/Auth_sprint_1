from datetime import datetime
from time import sleep
from typing import Generator

import clickhouse_connect
from backoff import expo, full_jitter, on_exception
from clickhouse_connect.driver import client as ClickhouseClient
from db_settings import settings
from loguru import logger
from models import Movie
from psycopg import ServerCursor, connect
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row
from storage import JsonFileStorage, State
from utils import FILM_WORK_QUERY, STATE_KEY, coroutine


@coroutine
@on_exception(expo, RuntimeError, jitter=full_jitter)
def fetch_changed_movies(
    cursor, next_node: Generator, batch_size: int = 100
) -> Generator[None, datetime, None]:
    while last_updated := (yield):
        logger.info(f"Fetching movies changed after {last_updated}")
        cursor.execute(FILM_WORK_QUERY, (last_updated,))
        while results := cursor.fetchmany(size=batch_size):
            next_node.send(results)


@coroutine
def transform_movies(next_node: Generator) -> Generator[None, list[dict], None]:
    while movie_dicts := (yield):
        batch = []
        for movie_dict in movie_dicts:
            logger.info(movie_dict)
            movie = Movie.model_validate(movie_dict)
            movie.title = movie.title.upper()
            logger.info(movie.model_dump())
            batch.append(movie)
        next_node.send(batch)


@coroutine
@on_exception(expo, RuntimeError, jitter=full_jitter)
def save_movies(
    state: State, clickhouse_engine: ClickhouseClient
) -> Generator[None, list[Movie], None]:
    while movies := (yield):
        logger.info(f"Received for saving {len(movies)} movies")
        if len(movies) == 0:
            continue

        movie_list = [list(movie.model_dump().values()) for movie in movies]

        clickhouse_engine.insert(
            "movie", movie_list, column_names=list(Movie.model_fields.keys())
        )
        state.set_state(STATE_KEY, str(movies[-1].modified))


if __name__ == "__main__":
    state = State(JsonFileStorage())
    dsn = make_conninfo(
        dbname=settings.postgres.db,
        host=settings.postgres.host,
        port=settings.postgres.port,
        user=settings.postgres.user,
        password=settings.postgres.password,
    )

    with connect(dsn, row_factory=dict_row) as conn, ServerCursor(
        conn, "fetcher"
    ) as cur, clickhouse_connect.get_client(
        host=settings.clickhouse.host,
        port=settings.clickhouse.port,
        database=settings.clickhouse.database,
    ) as clickhouse:
        saver_coro = save_movies(state, clickhouse)
        transformer_coro = transform_movies(next_node=saver_coro)
        fetcher_coro = fetch_changed_movies(cur, transformer_coro)

        while True:
            logger.info("Starting ETL process for updates ...")
            fetcher_coro.send(state.get_state(STATE_KEY) or str(datetime.min))
            sleep(20)
