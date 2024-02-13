import logging
import random
import time
from functools import wraps

from configs.test_settings import logger


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
        Декоратор для повторного выполнения функции
        в случае возникновения исключения
        использует экспоненциальную задержку + jitter
        но не более border_sleep_time
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    sleep_time = min(border_sleep_time, start_sleep_time * factor * attempt)
                    sleep_with_jitter = random.uniform(0, sleep_time)
                    logging.error(f"Error: {error}. Retrying in {sleep_with_jitter} seconds...")
                    time.sleep(sleep_with_jitter)
                    attempt += 1

        return inner

    return func_wrapper


@backoff()
def ping_service(some_service, service_name: str) -> int:
    if some_service.ping():
        logger.info(f"Соединение с {service_name} установлено.")
        some_service.close()
        return 1
    else:
        raise ConnectionError(f"Не удалось установить соединение с {service_name}.")
