import ast
import logging
import os
import signal
import sys
from types import FrameType

from configs.settings import get_settings
from models.enriching_message import EnrichingMessageTask
from pika.channel import Channel
from pika.spec import Basic, BasicProperties
from queues.rabbit_queue import RabbitQueue

logger = logging.getLogger('pre-sender-worker-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

worker_id = os.getenv("WORKER_ID", "worker_unknown")
rabbitmq_enriched = RabbitQueue(get_settings().get_rabbit_settings().enriched_queue)
rabbitmq_to_sending = RabbitQueue(get_settings().get_rabbit_settings().to_sending_key)


def handler(
        ch: Channel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes
):
    try:
        data = EnrichingMessageTask(**ast.literal_eval(body.decode()))

        logger.info(f"Processing task | pre_sender_worker | {data}")

        # тут мы проверяем можем ли мы отправлять сообщение или нет

        rabbitmq_to_sending.push(message=data)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error in callback: {e}")
        sys.stdout.flush()


try:
    rabbitmq_enriched.pop(handler=handler)
except Exception as e:
    logger.error(f"Error in worker: {e}")
