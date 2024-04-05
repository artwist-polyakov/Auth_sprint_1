import asyncio
import json
import time
import uuid
import clickhouse_connect
from core.settings import settings
from db.kafka_storage import get_kafka, KafkaRepository


def terrible_list_to_dict(data):
    result = []
    key = None

    for item in data:
        if item:  # if the item is not empty
            if item.startswith('\n') or key is None:
                key = item.strip()
            elif key:  # if it is a field type and we have a key
                result.append(
                    {
                        'name': key,
                        'type': item.strip(),
                        'nullable': 'Nullable' in item.strip()
                    }
                )
                key = None  # reset the key
    return result


class ETL:
    _kafka_bootstrap_servers = [f'{settings.kafka.host}:{settings.kafka.port}']

    def __init__(self):
        self._topics = ['player_events', 'view_events', 'custom_events']

    async def load(self, clickhouse, data, type):
        match (type):
            case 'player_events':
                # response = clickhouse.command(
                # f'DESCRIBE TABLE {f"{settings.clickhouse.database}.player_event"}'
                # )
                # print(terrible_list_to_dict(response))
                t = [(
                    uuid.uuid4(),
                    data['user_uuid'],
                    data['film_uuid'],
                    data['event_type'],
                    data['event_value'],
                    data['timestamp']
                )]
                print(t)
                clickhouse.insert(
                    f"{settings.clickhouse.database}.player_event",
                    t,
                    ['id', 'user_id', 'movie_id', 'type', 'event_value', 'timestamp']
                )
            case 'view_events':
                t = [(uuid.uuid4(), data['user_uuid'], data['film_uuid'], data['timestamp'])]
                print(t)

                clickhouse.insert(
                    f"{settings.clickhouse.database}.click",
                    t,
                    ['id', 'user_id', 'movie_id', 'timestamp']
                )
            case 'custom_events':
                t = [(uuid.uuid4(), data['user_uuid'], data['event_type'], (data['timestamp']))]
                print(t)

                clickhouse.insert(
                    f"{settings.clickhouse.database}.other_event",
                    t,
                    ['id', 'user_id', 'type', 'timestamp']
                )

    async def run(self, clickhouse):
        consumer = await get_kafka().consume()
        try:
            for msg in consumer:
                data = json.loads(msg.value.decode('utf-8'))
                topic = msg.topic
                if data is not None:
                    await self.load(clickhouse, data, topic)
                    await KafkaRepository.commit(consumer, msg)
        finally:
            consumer.close()


if __name__ == "__main__":
    print('ETL started')
    etl = ETL()
    time.sleep(20)
    with clickhouse_connect.get_client(
            host=settings.clickhouse.host,
            port=settings.clickhouse.port,
            database=settings.clickhouse.database,
            username=settings.clickhouse.etl_username,
            password=settings.clickhouse.etl_password,
    ) as clickhouse:
        print('Connected to Clickhouse')
        while True:
            print('ETL running')
            asyncio.run(etl.run(clickhouse))
