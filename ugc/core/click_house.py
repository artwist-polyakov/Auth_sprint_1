# # СИНХРОННЫЙ
# from clickhouse_driver import Client
# from settings import settings
#
# client = Client(host=settings.clickhouse.host)

# АСИНХРОННЫЙ
from aiochclient import ChClient
from aiohttp import ClientSession


async def main():
    async with ClientSession() as s:
        client = ChClient(s)
        assert await client.is_alive()  # возвращает True, если соединение успешно
