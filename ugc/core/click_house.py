# # СИНХРОННЫЙ
# import clickhouse_connect
# from settings import settings

# client = clickhouse_connect.get_client(
#             host=settings.clickhouse.host,
#             port=settings.clickhouse.port,
#             database=settings.clickhouse.database
#         )

# АСИНХРОННЫЙ
from aiochclient import ChClient
from aiohttp import ClientSession


async def main():
    async with ClientSession() as s:
        client = ChClient(s)
        assert await client.is_alive()  # возвращает True, если соединение успешно
