import asyncio
import logging
import time

from event_loader import EventLoader


async def main():
    loader = EventLoader()
    logging.info('Загружаю данные в Kafka...')
    await loader.load()

if __name__ == '__main__':
    time.sleep(5)
    asyncio.run(main())
