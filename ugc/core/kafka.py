from kafka import KafkaConsumer
from time import sleep

from settings import settings


connection = f'{settings.kafka.host}:{settings.kafka.port_4}'

producer = KafkaProducer(bootstrap_servers=[connection])

producer.send(
    topic='messages',
    value=b'my message from python',
    key=b'python-message',
)


consumer = KafkaConsumer(
    'messages',
    bootstrap_servers=[connection],
    auto_offset_reset='earliest',
    group_id='echo-messages-to-stdout',
)

sleep(1)

for message in consumer:
    print(message.value)