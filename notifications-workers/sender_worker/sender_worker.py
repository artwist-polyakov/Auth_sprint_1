import ast
import asyncio
import logging
import os
import signal
import sys
import time

from configs.settings import get_settings  # noqa
from models.enriching_message import EnrichingMessageTask
from queues.rabbit_queue import RabbitQueue  # noqa
from service.mail.fake_mail_service import FakeMailService  # noqa
from service.mail.smtp_mail_service import SMTPMailService  # noqa
from service.websocket.local_websocket_service import LocalWebsocketService

logger = logging.getLogger('creating-worker-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

worker_id = os.getenv("WORKER_ID", "worker_unknown")
rabbitmq_to_sending = RabbitQueue(
    get_settings().get_rabbit_settings().to_sending_queue
)
# mail_service = SMTPMailService()
mail_service = FakeMailService()
websocket_service = LocalWebsocketService()
loop = asyncio.get_event_loop()
loop.run_until_complete(websocket_service.connect())


def handle_exit(sig, frame):
    logger.info(f"{worker_id} received signal to terminate.")
    loop.run_until_complete(websocket_service.close())
    sys.exit(0)


data = {
    'title': 'Новое письмо!',
    'text': 'Произошло что-то интересное! :)',
    'image': 'https://pictures.s3.yandex.net:443/resources/news_1682073799.jpeg',
    'link_url': 'https://ya.ru',
    'link_text': 'Перейти на Яндекс'
}


def handler(ch, method, properties, body):
    try:
        data = EnrichingMessageTask(**ast.literal_eval(body.decode()))
        logger.info(f"Processing task {worker_id} | {data}")

        # тут мы отсылаем сообщение пользователю

    except Exception as e:
        print(f"Error in callback: {e}")
        sys.stdout.flush()


signal.signal(signal.SIGTERM, handle_exit)

try:
    mail_service.send(
        email="artwist@yandex.ru",
        subject=f"hello from worker {worker_id}",
        data=data,
        template="welcome"
    )
    while True:
        result = loop.run_until_complete(
            websocket_service.send_message(
                "artwist", "hello from worker"
            )
        )
        logger.info(f"Message sent: {result}")
        time.sleep(10)

    # rabbitmq_to_sending.pop(handler=handler)

except Exception as e:
    print(f"{worker_id} encountered an error: {e}")
    sys.stdout.flush()  # Принудительно записываем лог
    sys.exit(1)
