import asyncio
import logging

from event_loader import EventLoader


async def main():
    logging.warning('Загружаю данные в Kafka...')
    loader = EventLoader()
    await loader.load()

if __name__ == '__main__':
    asyncio.run(main())
