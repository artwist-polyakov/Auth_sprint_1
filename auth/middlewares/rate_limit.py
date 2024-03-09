# from fastapi import FastAPI, Request
#  from starlette.responses import JSONResponse
#  import redis
#  import uuid
#  import time
#
#  app = FastAPI()
#  redis_conn = redis.Redis(host='localhost', port=6379, db=0)
#
#  REQUEST_LIMIT_PER_MINUTE = 20
#  RATE_LIMIT_TTL = 60  # seconds
#
#  @app.middleware("http")
#  async def rate_limit_middleware(request: Request, call_next):
#      user_id = 'some_user_id'  # Получите ID пользователя, например из заголовк
#  запроса или сессии
#      x_request_id = str(uuid.uuid4())  # или используйте заголовок X-Request-Id
#  если он уже есть
#      key = f'{user_id}:requests'
#
#      # Добавляем X-Request-Id в список и обновляем TTL
#      pipe = redis_conn.pipeline()
#      pipe.lpush(key, x_request_id)
#      pipe.expire(key, RATE_LIMIT_TTL)
#      pipe.lrange(key, 0, -1)  # Получаем все элементы списка для подсчёта
#  количества запросов
#      _, _, current_requests = pipe.execute()
#
#      request_count = len(current_requests)
#
#      if request_count > REQUEST_LIMIT_PER_MINUTE:
#          # Если превышен лимит, возвращаем ошибку 429 без обработки запроса
#          return JSONResponse(
#              content={"message": "Too Many Requests"},
#              status_code=429,
#              headers={"X-Retry-After": str(RATE_LIMIT_TTL)}
#          )
#
#      # Обрабатываем запрос далее по цепочке
#      response = await call_next(request)
#
#      # Удаляем X-Request-Id из списка после обработки запроса
#      redis_conn.lrem(key, 1, x_request_id)
#
#      return response
#
# Обратите внимание, что это простейший пример миддлваре для ограничения запросов.
# В реальном приложении потребуется учитывать различные аспекты, такие как:
#
#  • Проверка идентификатора пользователя, чтобы применять ограничения на
#    индивидуальной основе.
#  • Использование асинхронного клиента Redis, если ваше приложение FastAPI
#    работает в асинхронном режиме.
#  • Безопасная обработка возможных ошибок соединения с Redis.
#
# Этот подход позволяет регистрировать активные запросы пользователя и удалять их
# при завершении. Операция LREM используется для удаления конкретного X-Request-Id
# из списка, что предотвращает ошибочное удаление запросов, которые были добавлены
# в список позже.`

# Для того чтобы выполнить удаление x_request_id из списка Redis через
# определенное время, вам нужно использовать механизм отложенной задачи. В
# контексте FastAPI вы можете использовать фоновые задачи (background tasks) для
# этой цели.
#
#                     Использование Background Tasks в FastAPI
#
# Чтобы использовать фоновые задачи в FastAPI, вам понадобится импортировать класс
# BackgroundTasks из модуля fastapi. Вот как это будет выглядеть на практике:
#                                                                          Block 2
#
#  from fastapi import FastAPI, Request, BackgroundTasks
#  from starlette.responses import JSONResponse
#  import redis
#  import uuid
#
#  app = FastAPI()
#  redis_conn = redis.Redis(host='localhost', port=6379, db=0)
#
#  REQUEST_LIMIT_PER_MINUTE = 20
#  RATE_LIMIT_TTL = 60  # Интервал времени для рейт-лимита (в секундах)
#  REMOVE_DELAY = 60  # Время задержки перед удалением X-Request-Id (в секундах)
#
#  async def remove_request_id(user_id: str, x_request_id: str):
#      await asyncio.sleep(REMOVE_DELAY)  # Используйте асинхронную паузу перед
#  удалением
#      redis_conn.lrem(f'{user_id}:requests', 1, x_request_id)
#
#  @app.middleware("http")
#  async def rate_limit_middleware(request: Request, call_next, background_tasks:
#  BackgroundTasks):
#      user_id = 'some_user_id'  # Получите ID пользователя
#      x_request_id = str(uuid.uuid4())  # Генерация уникального идентификатора д
#  запроса
#      key = f'{user_id}:requests'
#
#      # Добавляем X-Request-Id в список и обновляем TTL
#      pipe = redis_conn.pipeline()
#      pipe.lpush(key, x_request_id)
#      pipe.expire(key, RATE_LIMIT_TTL)
#      pipe.lrange(key, 0, -1)
#      _, _, current_requests = pipe.execute()
#
#      request_count = len(current_requests)
#
#      if request_count > REQUEST_LIMIT_PER_MINUTE:
#          return JSONResponse(content={"message": "Too Many Requests"},
#  status_code=429)
#
#      response = await call_next(request)
#
#      # Добавляем фоновую задачу для удаления X-Request-Id из списка через
#  REMOVE_DELAY секунд
#      background_tasks.add_task(remove_request_id, user_id, x_request_id)
#
#      return response
#
# background_tasks.add_task() добавляет функцию remove_request_id как фоновую
# задачу, которая будет выполнена после отправки ответа клиенту. Задержка
# реализуется с помощью асинхронной паузы await asyncio.sleep(REMOVE_DELAY) внутри
# функции remove_request_id.
#
# Обратите внимание, что для использования await в функции remove_request_id она
# должна быть асинхронной. Также если вы используете асинхронные операции с Redis,
# вы должны использовать асинхронный клиент, такой как aioredis.
#
# Теперь, когда запрос обрабатывается и отправляется через миддлваре, X-Request-Id
# будет удален из списка через заданное время ожидания, а не сразу.