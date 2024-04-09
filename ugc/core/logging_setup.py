import logging
import sys
from logging.handlers import RotatingFileHandler

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


def setup_root_logger():
    """Настройка конфигурации корневого логгера приложения"""

    # Настройка форматирования для логгера
    formatter = logging.Formatter(LOG_FORMAT)

    # Получение экземпляра корневого логгера
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)

    # Настройка консольного хэндлера
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Настройка хэндлера для записи в файл с ротацией
    file_handler = RotatingFileHandler(
        filename="./logs/logs.log",
        mode='a',
        maxBytes=15000000,
        backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
