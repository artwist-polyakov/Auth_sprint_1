from kafka import KafkaConsumer
import clickhouse_connect
import json
import asyncio

from core.settings import settings


class ETL:
    _kafka_bootstrap_servers = [f'{settings.kafka.host}:{settings.kafka.port}']

    def __init__(self):
        self.topics = ['player_events', 'view_events', 'custom_events']

    async def get_consumer(self):
        consumer_conf = {
            'bootstrap_servers': self._kafka_bootstrap_servers,
            'group_id': 'etl_group',
            'auto_offset_reset': 'earliest'
        }
        consumer = KafkaConsumer(*self.topics, **consumer_conf)
        return consumer

    async def transform(self, msg):
        if msg is None or msg.error():
            return None, None

        value = msg.value().decode('utf-8')
        event_data = json.loads(value)

        topic = msg.topic()
        if topic == 'player_events':
            event_type = 'PlayerEvent'
        elif topic == 'view_events':
            event_type = 'ViewEvent'
        elif topic == 'custom_events':
            event_type = 'CustomEvent'
        else:
            raise ValueError('Unknown event type')

        return event_data, event_type

    async def load(self, client, event_data, event_type):
        query = (f"INSERT INTO {settings.clickhouse.database}.events "
                 f"(event_id, event_type, event_data, event_timestamp) "
                 f"VALUES (?, ?, ?, NOW())")
        params = (event_data['event_id'], event_type, json.dumps(event_data))
        client.insert(query, params)

    async def run(self, clickhouse):
        consumer = await self.get_consumer()

        try:
            for msg in consumer:
                event_data, event_type = await self.transform(msg)
                if event_data is None:
                    continue

                await self.load(clickhouse, event_data, event_type)

        finally:
            consumer.close()


if __name__ == "__main__":
    etl = ETL()
    with clickhouse_connect.get_client(
        host=settings.clickhouse.host,
        port=settings.clickhouse.http_port,
        database=settings.clickhouse.database,
    ) as clickhouse:
        while True:
            asyncio.run(etl.run(clickhouse))
