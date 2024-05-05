import asyncio
import websockets

peoples = {}

async def welcome(websocket: websockets.WebSocketServerProtocol) -> str:
    await websocket.send('Представьтесь!') # Метод websocket.send отправляет сообщение пользователю
    name = await websocket.recv()  # websocket.recv ожидает получения сообщения
    await websocket.send('Чтобы поговорить, напишите "<имя>: <сообщение>". Например: Ира: купи хлеб.')
    await websocket.send('Посмотреть список участников можно командой "?"')
    peoples[name.strip()] = websocket
    return name

async def receiver(websocket: websockets.WebSocketServerProtocol, path: str) -> None: 
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
            else:
                await websocket.send(f'Пользователь {to} не найден')

# Создаём сервер, который будет обрабатывать подключения
ws_server = websockets.serve(receiver, "localhost", 8765)

# Запускаем event-loop
loop = asyncio.get_event_loop()
loop.run_until_complete(ws_server)
loop.run_forever()
