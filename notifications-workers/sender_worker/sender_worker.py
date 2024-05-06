import ast
import asyncio
import logging
import os
import signal
import sys

from configs.settings import get_settings  # noqa
from models.enriching_message import EnrichingMessageTask
from queues.rabbit_queue import RabbitQueue  # noqa
from service.mail.fake_mail_service import FakeMailService
from service.websocket.local_websocket_service import LocalWebsocketService

logger = logging.getLogger('creating-worker-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

worker_id = os.getenv("WORKER_ID", "worker_unknown")
rabbitmq_to_sending = RabbitQueue(
    get_settings().get_rabbit_settings().to_sending_queue
)
mail_service = FakeMailService()
websocket_service = LocalWebsocketService()
loop = asyncio.get_event_loop()
loop.run_until_complete(websocket_service.connect())


def handle_exit(sig, frame):
    logger.info(f"{worker_id} received signal to terminate.")
    loop.run_until_complete(websocket_service.close())
    sys.exit(0)


def handler(ch, method, properties, body):
    try:
        # получаем финальные данные из очереди на отправку
        data = EnrichingMessageTask(**ast.literal_eval(body.decode()))

        # формируем тело сообщения
        message_data = {
            'title': f'{data.title}',
            'text': f'{data.content}',
        }
        match data.type:
            case "email":
                mail_service.send(
                    email=data.contact,
                    subject=f"user {data.user_id}",
                    data=message_data,
                    template=data.scenario  # название темплейта = название сценария?
                )
            case "websocket":
                result = loop.run_until_complete(
                    websocket_service.send_message(
                        data.user_id,
                        f"Заголовок: {message_data['title']} | "
                        f"Текст: {message_data['text']}"
                    )
                )
                if not result:
                    ...
                    # нужно пометить как ошибочное в бд

        logger.info(f"Processing task | sender_worker | {message_data}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error in callback: {e}")
        sys.stdout.flush()


signal.signal(signal.SIGTERM, handle_exit)

try:
    rabbitmq_to_sending.pop(handler=handler)
except Exception as e:
    print(f"{worker_id} encountered an error: {e}")
    sys.stdout.flush()  # Принудительно записываем лог
    sys.exit(1)
