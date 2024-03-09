import asyncio
import logging
import random
import time
from functools import wraps

from db.cache.cache_storage import CacheStorage
from services.models.signup import CustomValueError

CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


def value_error_handler():
    """Декоратор для обработки ошибок валидации Pydantic."""

    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except CustomValueError as error:
                return {
                    'status_code': 422,
                    'content': str(error)
                }

        return inner

    return func_wrapper


def cached(result_type, cache_provider_attribute: str = "_cache"):
    """Декоратор для работы с данными кеша.

    result_type — сериализуемый и десериализуемый тип данных
    cache_provider_attribute — поле класса, содержащее объект реализующий интерфейс Redis.
    по уполчанию — _cache

    """

    def func_wrapper(func):
        @wraps(func)
        async def inner(self, *args, **kwargs):

            # собираем ключ
            class_name = self.__class__.__name__
            key = f"{class_name}:{func.__name__}:{args}:{kwargs}"

            # получаем провайдер кеша
            cache_storage = None
            if hasattr(self, cache_provider_attribute):
                t = getattr(self, cache_provider_attribute)
                # if issubclass(t.__class__, CacheStorage):
                if isinstance(t, CacheStorage):
                    cache_storage = t
                else:
                    logging.warning(f"Instance in {class_name}.{cache_provider_attribute} "
                                    f"is not instance of CacheStorage. It is {t.__class__}")

            # получаем данные из кеша
            result = await cache_storage.get_cache(key) if cache_storage else None
            if result:
                return result_type.parse_raw(result)
            result = await func(self, *args, **kwargs)

            # сохраняем в кеш
            if result and cache_storage:
                await cache_storage.put_cache(key, result.json(), expired=CACHE_EXPIRE_IN_SECONDS)

            # возвращаем результат
            return result

        return inner

    return func_wrapper


def backoff(max_attempts=-1, start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
        Декоратор для повторного выполнения функции
        в случае возникновения исключения
        использует экспоненциальную задержку + jitter
        но не более border_sleep_time
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            attempt = max_attempts
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    sleep_time = min(border_sleep_time, start_sleep_time * factor * attempt)
                    sleep_with_jitter = random.uniform(0, sleep_time)
                    attempt_string = f" Attempt {max_attempts - attempt + 1} " \
                        if max_attempts >= 0 else " "
                    logging.error(f"Error: {error}.{attempt_string}"
                                  f"Retrying in {sleep_with_jitter} seconds...")
                    time.sleep(sleep_with_jitter)
                    attempt -= 1 if max_attempts > 0 else 0
                    if attempt == 0:
                        logging.error(f"Error: {error}. No more attempts")
                        return None

        return inner

    return func_wrapper


def asyncbackoff(max_attempts=-1, start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
        Асинхронный декооратор для повторного выполнения функции
        в случае возникновения исключения
        использует экспоненциальную задержку + jitter
        но не более border_sleep_time
    """

    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            attempt = 0
            while max_attempts == -1 or attempt < max_attempts:
                try:
                    return await func(*args, **kwargs)
                except Exception as error:
                    attempt += 1
                    sleep_time = start_sleep_time * (factor ** attempt)
                    sleep_time = min(sleep_time, border_sleep_time)
                    sleep_with_jitter = random.uniform(0, sleep_time)
                    attempt_string = f"Attempt {attempt}" if max_attempts > 0 else ""
                    logging.error(f"Error: {error}.{attempt_string}"
                                  f"Retrying in {sleep_with_jitter} seconds...")
                    await asyncio.sleep(sleep_with_jitter)
            logging.error(f"Error: {error}. No more attempts")
            return None

        return inner

    return func_wrapper
