from kafka import KafkaConsumer
import clickhouse_connect
import json
import asyncio

from core.settings import settings
from db.kafka_storage import get_kafka


class ETL:
    _kafka_bootstrap_servers = [f'{settings.kafka.host}:{settings.kafka.port}']


    def __init__(self):
        self._topics = ['player_events', 'view_events', 'custom_events']

    async def load(self, clickhouse, data, type):
        # query = (f"INSERT INTO {settings.clickhouse.database}.events "
        #          f"(event_id, event_type, event_data, event_timestamp) "
        #          f"VALUES (?, ?, ?, NOW())")
        # params = (event_data['event_id'], event_type, json.dumps(event_data))
        # client.insert(query, params)

        match (type):
            case 'player_events':
                t = [data['user_uuid'], data['film_uuid'], data['event_type'], data['event_value'], data['timestamp']]
                clickhouse.insert(
                    f"{settings.clickhouse.database}.player_event",
                    t,
                    ['user_id', 'movie_id', 'type', 'event_value', 'timestamp']
                )
            case 'view_events':
                t = [data['user_uuid'], data['film_uuid'], data['timestamp']]
                clickhouse.insert(
                    f"{settings.clickhouse.database}.click",
                    t,
                    ['user_id', 'movie_id', 'timestamp']
                )
            case 'custom_events':
                t = [data['user_uuid'], data['event_type'], data['timestamp']]
                clickhouse.insert(
                    f"{settings.clickhouse.database}.other_event",
                    t,
                    ['user_id', 'type', 'timestamp']
                )




    async def run(self, clickhouse):
        for msg in await get_kafka().consume():
            data = msg.value.decode('utf-8')
            topic = msg.topic
            if data is not None:
                await self.load(clickhouse, data, topic)




if __name__ == "__main__":
    etl = ETL()
    with clickhouse_connect.get_client(
            host=settings.clickhouse.host,
            port=settings.clickhouse.port,
            database=settings.clickhouse.database,
            usename=settings.clickhouse.username,
            password=settings.clickhouse.password,
    ) as clickhouse:
        while True:
            asyncio.run(etl.run(clickhouse))
