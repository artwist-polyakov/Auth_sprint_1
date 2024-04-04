import datetime
import logging
from uuid import UUID

from kafka import KafkaConsumer
import clickhouse_connect
import json
import asyncio

from core.settings import settings

from db.models import PlayerEvent, Click, OtherEvent


class ETL:
    _kafka_bootstrap_servers = [f'{settings.kafka.host}:{settings.kafka.port}']

    def __init__(self):
        self.topics = ['player_events', 'click_events', 'other_events']
        self.events = {
            'click_events': {
                'table': 'click',
                'model': Click
            },
            'player_events': {
                'table': 'player_event',
                'model': PlayerEvent
            },
            'other_events': {
                'table': 'other_event',
                'model': OtherEvent
            }
        }

    async def get_consumer(self):
        consumer_conf = {
            'bootstrap_servers': self._kafka_bootstrap_servers,
            'group_id': 'etl_group',
            'auto_offset_reset': 'earliest'
        }
        consumer = KafkaConsumer(*self.topics, **consumer_conf)
        return consumer

    async def transform(self, msg):
        value = msg.value.decode('utf-8')
        event_data = json.loads(value)
        topic = msg.topic
        table = self.events.get(topic, {}).get('table')
        model = self.events.get(topic, {}).get('model')

        # formatted_time
        # timestamp_sec = msg.timestamp / 1000
        # formatted_time = datetime.datetime.fromtimestamp(timestamp_sec).strftime('%Y-%m-%d %H:%M:%S')
        return event_data, table, model

    async def load(self, client, event_data: dict, table: str, model):
        columns = list(model.model_fields.keys())
        logging.warning(columns)
        logging.warning(table)
        event = model(**event_data)
        data = list(event.model_dump().values())
        logging.warning(data)
        client.insert(table, data, column_names=columns)

    async def run(self, clickhouse):
        consumer = await self.get_consumer()

        try:
            for msg in consumer:
                event_data, table, model = await self.transform(msg)
                await self.load(
                    client=clickhouse,
                    event_data=event_data,
                    table=table,
                    model=model)

        finally:
            consumer.close()


if __name__ == "__main__":
    etl = ETL()
    with clickhouse_connect.get_client(
        host=settings.clickhouse.host,
        port=settings.clickhouse.port,
        database=settings.clickhouse.database,
    ) as clickhouse:
        while True:
            asyncio.run(etl.run(clickhouse))
            asyncio.sleep(5)
