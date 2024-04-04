import os
from datetime import datetime

import redis


class RedisCompanion:
    """
    Класс для работы с Redis.

    Умеет сказать когда было последнее обновление
    опеределенной таблицы
    и записать значение даты времени в Redis
    под ключом last_data_time

    Также может сохранить определенный набор строк в встроенную очередь
    И достать N элементов из очереди
    Также умеет проверять очередь на пустоту
    """

    _last_modified_key = "last_data_time_"
    _queue_key = "film_works_queue"
    _redis_settings = {
        "host": "redis",
        "port": os.getenv("REDIS_PORT"),
        "decode_responses": True,
    }

    def __init__(self):
        self.redis_connection = redis.Redis(**self._redis_settings)

    def save_update_time(self, for_table: str, update_time: datetime = datetime.now()):
        """Сохранить текущее время в Redis."""
        update_time_str = update_time.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        self.redis_connection.set(self._last_modified_key + for_table, update_time_str)

    def get_last_update(self, for_table: str) -> datetime | None:
        update_time_str = self.redis_connection.get(self._last_modified_key + for_table)
        return (
            datetime.strptime(update_time_str, "%Y-%m-%d %H:%M:%S.%f%z")
            if update_time_str
            else None
        )

    def save_to_queue(self, data: str):
        """Сохранить данные в очередь."""
        self.redis_connection.rpush(self._queue_key, data)

    def is_queue_empty(self) -> bool:
        """Проверить очередь на пустоту."""
        return self.redis_connection.llen(self._queue_key) == 0

    def is_queue_exists(self) -> bool:
        """Проверить существование очереди."""
        return self.redis_connection.exists(self._queue_key)

    def get_queue_size(self) -> int:
        """Получить длину очереди."""
        if self.is_queue_exists():
            return self.redis_connection.llen(self._queue_key)
        return -1

    def get_from_queue(self, count: int) -> list:
        """Получить N элементов из очереди."""

        if self.is_queue_empty() or (not self.is_queue_exists()):
            return []
        if count > self.get_queue_size():
            count = self.get_queue_size()
        result = self.redis_connection.lrange(self._queue_key, 0, count - 1)
        self.redis_connection.ltrim(self._queue_key, count, -1)
        return result
