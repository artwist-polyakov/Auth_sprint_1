import dataclasses
import datetime
import logging
import time
from dataclasses import dataclass
from typing import TypeVar

from models.postgres_models import (BatchUpdate, FilmworkToTransform,
                                    FilmWorkUpdate, GenreUpdate, PersonUpdate)
from psycopg2.extensions import connection as _connection
from utils.redis_companion import RedisCompanion
from utils.utils import backoff

T = TypeVar("T")


@dataclass
class QueryStruct:
    query: str
    params: tuple


class PostgresExtractor:
    """
    Класс для загрузки данных из Postgres и подготовке массива.

    для трансформации перед загрузкой в Elastic.

    Основная задача класса - получить данные из Postgres
    Для этого он выполняет 2 механики:

    1. Получает идентификаторы фильмов, которые были обновлены
    Для этого используется публичный метод reload_filmwork_ids

    Он работает очень просто:
    — проверяет очередь redis, если там есть элементы, то берет batch из них
    — если очередь пуста, то берет из Postgres через запрос свежих обновлений
    по трём тбалицам: film_work, person, genre от старых обновлений к новым.
    — если в Postgres нет обновлений, то возвращает пустой массив
    — если в получившихся данных обновлений слишком много, то берет только первые batch,
    а остальные кладет в очередь redis

    2. Получает данные по идентификаторам фильмов
    """

    # временно сохраняет последние максимальные даты обновлений,
    # чтобы не делать запросы в Postgres старше них
    _last_modifieds_to_save: dict[str, datetime] = {}

    _redis_companion = RedisCompanion()

    # временно сохраняет новые максимальные даты обновлений,
    # чтобы сохранить их после успешного цикла обновлений
    _new_modifieds_to_save: dict[str, datetime] = {}  # todo возможно не нужно

    # имена таблиц в которых ищем обновления
    _tables: list[str] = ["film_work", "person", "genre"]

    # маппинг первичных ключей для таблиц,
    # так как мы в итоге должны получить идентификаторы и фильмов и персон
    # и жанров, в одном массиве
    _primary_keys_map: dict[str, str] = {
        "film_work": "fw_id",
        "person": "person_id",
        "genre": "genre_id",
    }

    # таблица для запросов к бд
    _tables_query_map: dict[str, str] = {}

    # используем множество, чтобы не загружать повторно один фильм
    _set_for_extraction: set[str] = set()

    # заготовка данных для передачи в загрузчик
    _batch_update: BatchUpdate = BatchUpdate()

    def __init__(self, pg_conn: _connection, batch_size: int = 10):
        self._pg_conn = pg_conn
        self._batch_size = batch_size
        self._refresh_last_modifieds()
        self._configure_query_map()
        self.reload_filmwork_ids()

    @backoff()
    def reload_filmwork_ids(self):
        self._set_for_extraction = set()
        if self._redis_companion.is_queue_exists():
            self._set_for_extraction = set(
                self._redis_companion.get_from_queue(self._batch_size)
            )
        else:
            self._get_updates_from_database()

    @backoff()
    def _get_updates_from_database(self):
        # получаем BATCH обновлений для фильмов из PSQL
        filmwork_updates = self._get_updates("film_work", FilmWorkUpdate)
        self._process_filmwork_updates(filmwork_updates)

        # получаем BATCH обновлений для персон из PSQL
        persons_updates = self._get_updates("person", PersonUpdate)

        # сохраняем их в заготовку для передачи в загрузчик
        # эта порция данных отправится с индекс по персонам
        self._batch_update.person_data = persons_updates

        # получаем идентификаторы фильмов связанных с обновившимися персонами
        # для них тоже надо записать обновление.
        persons_ids = [p.id for p in persons_updates]
        if len(persons_ids) > 0:
            query = self._get_query_to_load_ids_throw_relation(
                persons_ids,
                "person_film_work",
                "person",
                "person_id",
            )
            request = QueryStruct(query, tuple(persons_ids))
            filmwork_updates = self._get_updates("film_work", FilmWorkUpdate, request)
            self._process_filmwork_updates(filmwork_updates)

        # получаем BATCH обновлений для жанров из PSQL
        genres_updates = self._get_updates("genre", GenreUpdate)

        # сохраняем их в заготовку для передачи в загрузчик
        # эта порция данных отправится с индекс по жанрам
        self._batch_update.genre_data = genres_updates

        # получаем идентификаторы фильмов связанных с обновившимися жанрами
        # для них тоже надо записать обновление.
        genres_ids = [g.id for g in genres_updates]
        if len(genres_ids) > 0:
            query = self._get_query_to_load_ids_throw_relation(
                genres_ids,
                "genre_film_work",
                "genre",
                "genre_id",
            )
            request = QueryStruct(query, tuple(genres_ids))
            filmwork_updates = self._get_updates("film_work", FilmWorkUpdate, request)
            self._process_filmwork_updates(filmwork_updates)

        # распределяем полученные идентификаторы фильмов на процессинг и очередь
        self._set_for_extraction = self._move_overquantity_to_queue(
            list(self._set_for_extraction)
        )

    @backoff()
    def _move_overquantity_to_queue(self, data: list[str]):
        if len(data) > self._batch_size:
            for item in data[self._batch_size:]:
                self._redis_companion.save_to_queue(item)
            return data[: self._batch_size]
        return data

    def _process_filmwork_updates(self, filmwork_updates: list[FilmWorkUpdate]):
        for fw in filmwork_updates:
            # фиг знает откуда пустые значения взялись
            if fw.id != "":
                self._set_for_extraction.add(fw.id)

    def _configure_query_map(self):
        for table_name in self._tables:
            self._tables_query_map[table_name] = self._get_query_for_updated_ids(
                table_name, self._primary_keys_map[table_name]
            )

    @backoff()
    def extract_filmworks(self) -> BatchUpdate:
        # запишем новые ключи для редиса
        self._batch_update.new_keys_for_redis = self._new_modifieds_to_save
        for_ids = list(self._set_for_extraction)
        if not for_ids:
            time.sleep(30)  # если данные не приходят, можно и полминуты отдохнуть
            return self._batch_update

        cursor = None
        try:
            cursor = self._pg_conn.cursor()
            cursor.execute(
                self._get_query_to_load_all_new_data(for_ids), tuple(for_ids)
            )
            while data := cursor.fetchmany(self._batch_size):
                self._batch_update.film_work_data += [
                    FilmworkToTransform(**row) for row in data
                ]
            return self._batch_update
        except Exception as e:
            logging.error(e)
            self._pg_conn.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()

    @backoff()
    def _refresh_last_modifieds(self):
        for table_name in self._tables:
            self._last_modifieds_to_save[table_name] = (
                self._redis_companion.get_last_update(table_name)
                or datetime.datetime.min
            ).strftime("%Y-%m-%d %H:%M:%S.%f%z")

    def _get_updates(
        self, table_name: str, dataclass_name: T, query: QueryStruct | None = None
    ) -> list[T]:
        cursor = None
        fields = {f.name for f in dataclasses.fields(dataclass_name)}
        try:
            cursor = self._pg_conn.cursor()
            if query:
                cursor.execute(query.query, query.params)
            else:
                cursor.execute(
                    self._tables_query_map[table_name],
                    (self._last_modifieds_to_save[table_name],),
                )
            result = []
            while data := cursor.fetchmany(self._batch_size):
                data = [
                    {key: value for key, value in row.items() if key in fields}
                    for row in data
                ]
                result += [dataclass_name(**row) for row in data]
            if result:
                self._new_modifieds_to_save[table_name] = result[-1].modified
            return result
        except Exception as e:
            logging.error(e)
            self._pg_conn.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()

    def _get_query_for_updated_ids(
        self, table_name: str, primary_key_field_name
    ) -> str:
        query_string = f"""
SELECT * FROM content.{table_name}
WHERE modified > %s
ORDER BY modified ASC
LIMIT {self._batch_size}
        """
        return query_string

    def _get_query_to_load_all_new_data(self, ids: list[str] = []) -> str:
        if ids:
            placeholders = ", ".join(["%s"] * len(ids))
            query_string = f"""
SELECT
    fw.id as id,
    fw.title as title,
    fw.description as description,
    fw.rating as rating,
    fw.type as type,
    fw.created as created,
    fw.modified as modified,
    pfw.role as role,
    p.id as person_id,
    p.full_name as person_full_name,
    g.id as genre_id,
    g.name as genre_name,
    g.description as genre_description
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE fw.id IN ({placeholders})
            """
            return query_string
        else:
            raise Exception("ids is empty")

    def _get_query_to_load_ids_throw_relation(
        self,
        ids: list[str],
        relations_table_name: str,
        join_table_name: str,
        condition_field_name: str,
    ) -> str:
        placeholders = ", ".join(["%s"] * len(ids))
        query_string = f"""
SELECT fw.id as id, fw.modified
FROM content.film_work fw
LEFT JOIN content.{relations_table_name} r ON r.film_work_id = fw.id
WHERE r.{condition_field_name} IN ({placeholders})
ORDER BY fw.modified ASC
        """
        return query_string
