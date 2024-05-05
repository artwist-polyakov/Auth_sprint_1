import asyncio
import websockets  # Установите этот пакет, если у вас его нет
import logging

logging.basicConfig(level=logging.INFO)

peoples = {}  # Словарь будет содержать ник подключившегося человека и указатель на его websocket-соединение.


# Это понадобится для маршрутизации сообщений между пользователями

async def welcome(websocket: websockets.WebSocketServerProtocol) -> str:
    name = await websocket.recv()  # websocket.recv ожидает получения сообщения
    peoples[name.strip()] = websocket
    return name


async def receiver(websocket: websockets.WebSocketServerProtocol, path: str) -> None:
    name = None
    try:
        name = await welcome(websocket)
        while True:
            # Получаем сообщение от абонента и решаем, что с ним делать
            message = (await websocket.recv()).strip()
            if message == '?':  # На знак вопроса вернём список ников подключившихся людей
                await websocket.send(', '.join(peoples.keys()))
                continue
            else:  # Остальные сообщения попытаемся проанализировать и отправить нужному собеседнику
                to, text = message.split(': ', 1)
                if to in peoples:
                    # Пересылаем сообщение в канал получателя, указав отправителя
                    await peoples[to].send(f'Сообщение от {name}: {text}')
                    await websocket.send(f'ОК')
                else:
                    await websocket.send(f'BAD')
    except websockets.exceptions.ConnectionClosed as e:
        logging.info(f"Connection with {name.strip()} closed: {e}")
        peoples.pop(name.strip(), None)
        logging.info(f"{name.strip()} has been disconnected and removed from the list.")


# Создаём сервер, который будет обрабатывать подключения
ws_server = websockets.serve(receiver, "0.0.0.0", 8765)

# Запускаем event-loop
loop = asyncio.get_event_loop()
loop.run_until_complete(ws_server)
loop.run_forever()
