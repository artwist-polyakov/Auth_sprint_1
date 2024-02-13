import asyncio
import subprocess

from configs.test_settings import logger


async def main():
    logger.info('Загружаю тестовые данные в Elasticsearch...')

    logger.info('Тестовые данные загружены. Начинаю тесты...')

    tests_directory = './src/'
    result = subprocess.run(['pytest', tests_directory])
    logger.info(result)

    logger.info('Конец выполнения тестов')


if __name__ == '__main__':
    asyncio.run(main())
