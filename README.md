Ссылка на приватный репозиторий с командной работой https://github.com/artwist-polyakov/Auth_sprint_1

> Просим прощения за возможные небрежности — делали проект вдвоем.

# Проектная работа 10 спринта

## Папки и контейнеры этого спринта

 - `/ws` — сервер вебсокетов, запускается в контейнере `ws`
 - `/etl-notifications-tasks` — задачи для ETL, запускаются в контейнерах `etl-notifications-tasks`. Стартует по крону раз в минуту.
 - `/notifications-workers` — воркеры для обработки задач, запускаются в контейнерах `notifications-workers`
 - `/notifications` — сервис уведомлений, запускается в контейнере `notifications`
 - `/rabbitmq` — RabbitMQ, запускается в контейнере `rabbitmq` и `rabbitmq-init`
 - есть контейнер для базы данных `notifications-db` — она партицирована по дате для поиска уведомлений.
Миграции запускаются в контейнере `notifications`. База для вебсокетов излишняя, сервер вебсокетов сам хранит и удаляет пользователей.



## Запуск проекта

1. Cкопируйте переменные окружения из файла `.env.example` в файл `.env`
2. Запустите проект командой `docker-compose up -d --build`

## Схема работы приложения

Расположена в папке `docs/c2-notifications.puml`

Или если нужна картинка то `docs/c2-notifications-_b_Movies_notifications_pipeline__b_.png`

## АПИ для поставновки задач нотификаций 

1. Доступен по адресу http://localhost:8000/notifications/openapi
2. Позволяет отправить задачу на постановку в очередь
3. Позволяет получить статус задачи по id
4. Чтобы запустить задачу — надо выбрать письмо email или webosocket (`push`) (я понимаю что вебсокет — не пуш, но модель данных вышла такая, простите )
5. С другими типами уведомлений ничего не происходит — помечаеются в базе как ошибка.
6. Если зарегистрироваться в сервисе, то запускается процесс отправки письма на почту — письмо появится в папке `./mailings`

> Описал детально все ниже.


## Rabbit MQ

1. Интерфейс ребита доступен по адресу http://localhost:15672/

## Уведомления на почту

1. Пока у нас нет доступа к почтовому серверу, поэтому уведомления отправляются в директорию `./mailings`

2. Письма можно открыть в почтовом клиенте.
3. 6 мая яндекс разблокировал почтовый ящик, я обещали что буду слать почту только на `master@artwist.ru` или на `artwist@yandex.ru`.
Думаю что можно одно письмо и на другой аккаунт отправить, но для того чтобы это заработало, надо раскомментировать в проекте `mail_service = SMTPMailService()` в файле `sender_worker.py`

## Websocket клиент

1. Чтобы получать уведомления по вебсокет вам надо установить утилиту `websocat`.

https://github.com/vi/websocat

2. Далее в терминале после заупуска контейнеров подключаемся к вебсокету

```shell

websocat ws://localhost:8765

```

3. После того как вы авторизовались в апи авторизации
http://localhost:8000/auth/openapi#/Users/sign_up_auth_v1_users_sign_up_post

> **при запуске бота напишите ему свой uuid.**
> 
> Бот не реагирует на сообщение, но запомнит вас.


## Ci/CD

Оставили из прошлого спринта.

# Проектная работа 9 спринта

## CI/CD

1. Добавлены файлы `.github/workflows` для автоматического тестирования
2. Тестируется установка зависимостей на Python 3.10, 3.11 + flake8
3. Если добавить проверку 3.9 — то flake вернет Syntax error из-за использования конструкции `match-case` внедренной в 3.10
4. Чтобы получать уведомления в телеграм, надо вступить в группу https://t.me/+34kxKhiOTmpiNjE6

## ELK

1. Если у вас платформа MacOS M1 — то надо раскоментировать строку докерфайла `platform: linux/amd64` для сервиса `filebeat`
2. Добавлены файлы конфигурации для `filebeat`, `logstash`, `kibana`
3. Чтобы настроить кибану надо создать индекс: `Stack Management > Data views`
http://localhost:5601/app/management/kibana/indexPatterns
4. Отправьте какое-либо событие через сервис UGC, либо сделайте запрос на авторизацию или фильмы, чтобы увидеть лог в кибане

## Sentry

Доступы к Sentry:

master@artwist.ru
Qhi84DVW@XKaXsx

Чтобы не пытаться вызывать ошибку сервера, можно добавить куда-нибудь `1/0` и посмотреть логи в Sentry
Я добавил их закомментированными в апишке ugc

## MONGO vs ELASTIC (под нагрузкой)

Инструкция по запуску тестов под нагрузкой:

```shell
cd ./research
guidance.md
```

Результаты на локальном компьютере были следующие

MONGO
Среднее время записи в сек.(10000 - строк | 10 - итераций): 0.14699999999720603
Среднее время записи в сек.(100000 - строк | 10 - итераций): 1.3764000000082888
Среднее время чтения в сек.(1000000 - строк): 1.117200000002049
ELASTIC
Среднее время записи в сек.(10000 - строк | 10 - итераций): 0.4686000000103377
Среднее время записи в сек.(100000 - строк | 10 - итераций): 3.423700000002282
Среднее время чтения в сек.(1000000 - строк): 0.19690000000409782

Запись в рамках тестов лучшие результаты показывает МОНГО почти в 3 раза,
но в случае чтения данных ЕЛАСТИК опережает больше чем в 5 раз

так как нам надо будет чаще читать, чем писать — выбираем эластика
Для хранения пользовательских данных, таких как лайки, закладки страниц и рецензии на фильмы,
MongoDB может быть более предпочтительным выбором, особенно если эти операции преимущественно
связаны с записью и обновлением данных и не требуют сложных поисковых возможностей.

Так же с МОНГО проще работать, в связи с выше укзанными причинами было принято решение
реализовать новые ручки на МОНГО

## Отдельный сервис vs Добавление в уже существующий
### Создание Отдельного Сервиса

Плюсы:
1. Модульность: Сервисы, специализирующиеся на определенных задачах, легче поддерживать и масштабировать.
2. Независимость Разработки: Разные команды могут работать параллельно над разными сервисами.
3. Упрощение Тестирования: Отдельные сервисы можно тестировать отдельно друг от друга.

Минусы:
1. Сложность Управления: Больше сервисов - сложнее управлять инфраструктурой.
2. Задержки: Возможно увеличение задержек из-за взаимодействия между сервисами.
3. Дублирование Кода: Возможно возникновение дублирования кода между сервисами.

### Добавление в Существующий Сервис

Плюсы:
1. Простота Развертывания: Одно приложение легче развернуть и управлять.
2. Общая База Кода: Легче поддерживать и обновлять при единой базе кода.
3. Экономия Ресурсов: Меньше затрат на инфраструктуру и управление.

Минусы:
1. Сложность Кода: Приложение может стать слишком сложным и тяжелым для понимания.
2. Риск "Точки Отказа": Ошибка в одной части системы может повлиять на всё приложение.
3. Ограниченная Масштабируемость: Масштабировать отдельные компоненты приложения может быть сложнее.

Принимая во внимание текущую архитектуру системы и необходимость интеграции с Kafka, Clickhouse, и MongoDB, расширение существующего сервиса является предпочтительным вариантом.

# Проектная работа 8 спринта

## Функциональные требования

### Клиент статистики (только для авторизованнных)
- Записывать события просмотра фильмов (uuid фильма)
- Записывать события взаимодействия с плеером (пауза, воспроизведение, изменение качества, изменение перевода, просмотр отдельной секунды)
- Записывать произвольные действия пользователя через передачу произвольного ключа.

### Клиент аналитики

- Может подключиться к базе данных с доступом только на чтение


## Нефункциональные требования

- Падение сервиса не должно приводить к падению других сервисов
- Время ответа 95% запросов не должно превышать 100 мс
- Время ответа 99% запросов не должно превышать 200 мс
- Доступность 99.9%
- Ожидаемая нагрузка 1000 RPS
- Пиковая нагрузка 4000 RPS

## Архитектура

— Сервис 1: UGC-сервис на flask

Умеет проверять авторизован ли пользователь и его uuid.
Позволяет передать некоторое событие:
- Просмотр фильма (uuid фильма, uuid пользователя)
- Взаимодействие с плеером (uuid фильма, uuid пользователя, действие enum)
- Произвольное действие (uuid пользователя, ключ, значение)

— Сервис 2: Stat-сервис на flask
Умеет складывать событие в кафку

— Сервис 3: Kafka

Хранит очереди сообщений
Разделение очередей продумывает ответственный за кафку.

— Сервис 4: Скрипт etl между кафкой и olap для записи сообщений

Умеет забрать событие и преобразовать его в запись в колоночной субд

— Сервис 5. Кликхаус для хранения данных аналитки.

# ИТОГО по спринту 8

1. Описаны схема модуля статистики и его API в папке `./docs

Для просмотра документации следует установить поддержку UML на устройство https://plantuml.com/ru/starting

2. Запуск контейнеров с сервисами

```shell
docker-compose up -d --build
```

3. Добавлен сервис UGC — http://localhost:8000/ugc/openapi/swagger
4. Локуст для проверки нагрузки на сервис UGC — http://localhost:8089/

пользователей 3000

Ramp 200

Host: http://ugc:5555

![](https://media.cleanshot.cloud/media/7299/DlMJy5Smw82oFlqC3hwKvMHr1MRTFLRwd2kwH9E6.jpeg?Expires=1712285686&Signature=bJX71nMO~93ACgYEuC4stV9tkkT~62HbqZLkf4ZYhiXRJBEUwt-PzAVaxopMFhKNR13BMfOp2rhsfOz~BG9gHiwXRQAYQD0H1eBaOSQNAh18uQVCPpCBEPvBPZVzcvXRiFFLHLOZySCKRNL-3HXHporaa5GSWOfWu0kpj3TVM6Re4u6k9tB32fHSI35XYRWmdb-nH4peBeP5ozH0IRNO~zy0-WJfUox1bSYNF1tipIRi1xlpfL1Jzo-TKQZFz5aZvijvDkr2UaMdbVJFXJ-4MKa67a0huboKYZNUkMK8JKW61Zv8MdAGPsYzLxLly83bBOhHk-r-lixtAtPSb2Wf6Q__&Key-Pair-Id=K269JMAT9ZF4GZ)


# Проектная работа 7 спринта

## Интеграция Auth-сервиса с сервисом выдачи контента

1. Создан middleware проверки прав пользователя `./movies/middlewares/rbac.py`

2. Добавлена изящная деградация `./movies/middlewares/rbac.py`. Возвращаем поиск по звёздным войнам в ответ на любой запрос.

3. Проверка доступа (`./auth/api/v1/users.py` `def check_permissions`) может проводиться с помощью токена

4. В настройки (`./movies/configs/settings.py`) добавлен внутренний токен для обхода middleware rbac `internal_secret_token`

## Интеграция Auth-сервиса с административной панелью

1. Создан контейнер `admin` с сервисом `django`, создано приложение `users`, внесены изменения в `nginx.conf`
2. Изменена модель по умолчанию User `./admin/users/models.py`

Доступ к панели администратора имеют (`./admin/users/backends.py`):
- пользователи, являющиеся superuser
- администраторы, имеющие право на доступ к ресурсу `admin`

## Jaeger

1. Создан контейнер `jaeger`

2. Настроена трассировка `./auth/main.py`, `./movies/main.py`, `nginx/nginx.conf`


## Rate limit

В сервисе авторизации добавлена возможность ограничения количества запросов к серверу для предотвращения перебора паролей.
Для этого используется redis и методы `zadd`, `zremrangebyscore`, `zcard`

Чтобы избежать засорения каждую минуту запускается `cleanup_task`, которая применяет `zremrangebyscore`.

## Oauth 2.0

Используем сервис Яндекса.

Страница авторизации https://oauth.yandex.ru/authorize?response_type=code&client_id=f0f7d3c997d14831944552f7739d94c2
Соглашаемся с предоставлением доступа, нас перенаправляют на страницу апи, которая выпускает токен доступа и рефреш токен.

1. Создана api `yandex_login` (`./auth/api/v1/users.py`)

2. Функция для обмена кода на токены `exchange_code_for_tokens` (`./auth/api/v1/users.py`)

3. Созданы абстрактный класс OAuthService (`./auth/db/oauth/oauth_service.py`) и класс `YandexOAuthService` (`./auth/db/oauth/yandex_oauth_service.py`). Созданы методы, позволяющие получать пользовательскую информацию

4. Создана модель токена `./auth/db/models/token_models/oauth_token.py`

5. Созданы модель пароля и метод, умеющий генерировать валидный пароль `./auth/services/models/signup.py`

6. Создана модель для хранения oauth данных `./auth/db/auth/yandex_oauth.py`

7. Реализованы изменения, связанные с работой oauth `./auth/db/postgres.py`, `./auth/services/user_service.py`

## Партицирование Refresh Token (истории входов)

Партицирование истории входов по `user_device_type`

1. Изменена модель RefreshToken `./auth/db/auth/refresh_token.py`

2. Созданы дополнительные миграции `./auth/migrations/`, в том числе был создан индекс `ix_refresh_tokens_user_device_type`

3. Создана функция для определения типа устройства `./auth/api/v1/users.py` `get_device_type`

## Описание задания

1. Создайте интеграцию Auth-сервиса с сервисом выдачи контента и административной панелью, используя контракт, который вы сделали в прошлом задании.
При создании интеграции не забудьте учесть изящную деградацию Auth-сервиса. Auth сервис — один из самых нагруженных, потому что в него ходят большинство сервисов сайта. И если он откажет, сайт отказать не должен. Обязательно учтите этот сценарий в интеграциях с Auth-сервисом.

2. Добавьте в Auth-сервис трассировку и подключите к Jaeger. Для этого вам нужно добавить работу с заголовком x-request-id и отправку трассировок в Jaeger.

3. Добавьте в сервис механизм ограничения количества запросов к серверу.

4. Упростите регистрацию и аутентификацию пользователей в Auth-сервисе, добавив вход через социальные сервисы. Список сервисов выбирайте исходя из целевой аудитории онлайн-кинотеатра — подумайте, какими социальными сервисами они пользуются. Например, использовать OAuth от Github — не самая удачная идея. Ваши пользователи — не разработчики и вряд ли пользуются аккаунтом на Github. Лучше добавить Yandex, VK или Google.
 Вам не нужно делать фронтенд в этой задаче и реализовывать собственный сервер OAuth. Нужно реализовать протокол со стороны потребителя.

5. Партицируйте таблицу с пользователями или с историей входов. Подумайте, по каким критериям вы бы её разделили. Важно посмотреть на таблицу не только в текущем времени, но и заглядывая в некое будущее, когда в ней будут миллионы записей. Пользователи могут быть из одной страны, но из разных регионов. А ещё пользователи могут использовать разные устройства для входа и иметь разные возрастные ограничения.



# Проектная работа 6 спринта

## Развёртывание проекта

1. Склонируйте репозиторий
2. Скачайте файл с настройками окружения [по ссылке](https://disk.yandex.ru/d/EqKF0k8QJgGKQA). Пароль `1234`
3. Скачайте файлы сертификатов [по ссылке](https://disk.yandex.ru/d/7YHy0fzdMUg-rQ). Пароль `1234`
4. корневой папке проекта разместите файл `.env` с переменными окружения. Пример файла находится в `.env.example`.
5. В папке /nginx/ssl разместите файлы сертификатов скачанных в п.2
6. Запустите проект командой `docker-compose up -d --build`
7. Приложение будет доступно по адресам:

если не нужен SSL
- http://localhost:8000/auth/openapi
- http://localhost:8000/api/openapi

если установили сертификаты
- https://localhost/auth/openapi
- https://localhost/api/openapi

Необходмо согласиться с недостоверным сертификатом или добавить самоподписанный сертификат по инструкции в файле `FOR_TEAM.md`

## Работа с ролями

Упрялять ролями могут только суперпользователи.
Для создания суперпользователя используйте команду:

```shell

docker exec -it auth python superuser.py <email> <pass>

```

## Описание задания

С этого модуля вы больше не будете получать чётко расписанное ТЗ, а задания для каждого спринта вы найдёте внутри уроков. Перед тем как начать программировать, вам предстоит продумать архитектуру решения, декомпозировать задачи и распределить их между командой.

В первом спринте модуля вы напишете основу вашего сервиса и реализуете все базовые требования к нему. Старайтесь избегать ситуаций, в которых один из ваших коллег сидит без дела. Для этого вам придётся составлять задачи, которые можно выполнить параллельно и выбрать единый стиль написания кода.

К концу спринта у вас должен получиться сервис авторизации с системой ролей, написанный на FastAPI. Первый шаг к этому — проработать и описать архитектуру вашего сервиса. Это значит, что перед тем, как приступить к разработке, нужно составить план действий: из чего будет состоять сервис, каким будет его API, какие хранилища он будет использовать и какой будет его схема данных. Описание нужно сдать на проверку наставнику. Вам предстоит выбрать, какой метод организации доступов использовать для онлайн-кинотеатра, и систему прав, которая позволит ограничить доступ к ресурсам.

Для описания API рекомендуем использовать [OpenAPI](https://editor.swagger.io){target="_blank"}, если вы выберете путь REST. Или используйте текстовое описание, если вы планируете использовать gRPC. С этими инструментами вы познакомились в предыдущих модулях. Обязательно продумайте и опишите обработку ошибок. Например, как отреагирует ваш API, если обратиться к нему с истёкшим токеном? Будет ли отличаться ответ API, если передать ему токен с неверной подписью? А если имя пользователя уже занято? Документация вашего API должна включать не только ответы сервера при успешном завершении запроса, но и понятное описание возможных ответов с ошибкой.

Для успешного завершения первой части модуля в вашем сервисе должны быть реализованы API для аутентификации и система управления ролями. Роли понадобятся, чтобы ограничить доступ к некоторым категориям фильмов. Например, «Фильмы, выпущенные менее 3 лет назад» могут просматривать только пользователи из группы 'subscribers'.

**API для сайта и личного кабинета**

- регистрация пользователя;
- вход пользователя в аккаунт (обмен логина и пароля на пару токенов: JWT-access токен и refresh токен);
- обновление access-токена;
- выход пользователя из аккаунта;
- изменение логина или пароля (с отправкой email вы познакомитесь в следующих модулях, поэтому пока ваш сервис должен позволять изменять личные данные без дополнительных подтверждений);
- получение пользователем своей истории входов в аккаунт;

**API для управления доступами**

- CRUD для управления ролями:
  - создание роли,
  - удаление роли,
  - изменение роли,
  - просмотр всех ролей.
- назначить пользователю роль;
- отобрать у пользователя роль;
- метод для проверки наличия прав у пользователя.

**Подсказки**

1. Продумайте, что делать с анонимными пользователями, которым доступно всё, что не запрещено отдельными правами.
2. Метод проверки авторизации будет всегда нужен пользователям. Ходить каждый раз в БД — не очень хорошая идея. Подумайте, как улучшить производительность системы.
3. Добавьте консольную команду для создания суперпользователя, которому всегда разрешено делать все действия в системе.
4. Чтобы упростить себе жизнь с настройкой суперпользователя, продумайте, как сделать так, чтобы при авторизации ему всегда отдавался успех при всех запросах.
5. Для реализации ограничения по фильмам подумайте о присвоении им какой-либо метки. Это потребует небольшой доработки ETL-процесса.

**Дополнительное задание**

Реализуйте кнопку «Выйти из остальных аккаунтов», не прибегая к хранению в БД активных access-токенов.
