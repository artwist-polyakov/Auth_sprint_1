from kafka import KafkaConsumer
from time import sleep


producer = KafkaProducer(bootstrap_servers=['localhost:9094'])

producer.send(
    topic='messages',
    value=b'my message from python',
    key=b'python-message',
)


consumer = KafkaConsumer(
    'messages',
    bootstrap_servers=['localhost:9094'],
    auto_offset_reset='earliest',
    group_id='echo-messages-to-stdout',
)

sleep(1)

for message in consumer:
    print(message.value)