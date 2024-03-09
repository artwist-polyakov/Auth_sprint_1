Ссылка на приватный репозиторий с командной работой https://github.com/artwist-polyakov/Auth_sprint_1

# Проектная работа 7 спринта

## Интеграция Auth-сервиса с сервисом выдачи контента

1. Создан middleware проверки прав пользователя `./movies/middlewares/rbac.py`

2. Добавлена изящная деградация `./movies/middlewares/rbac.py`

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



## Oauth 2.0

Используем сервис Яндекса.

Страница авторизации https://oauth.yandex.ru/authorize?response_type=code&client_id=f0f7d3c997d14831944552f7739d94c2
Соглашаемся с предоставлением доступа, нас перенаправляют на страницу апи, которая выпускает токен доступа и рефреш токен.

1. Создана api `yandex_login` (`./auth/api/v1/users.py`)

2. Функция для обмена кода на токены `exchange_code_for_tokens` (`./auth/api/v1/users.py`)

3. Созданы абстрактный класс OAuthService (`./auth/db/oauth/oauth_service.py`) и класс `YandexOAuthService` (`./auth/db/oauth/yandex_oauth_service.py`). Созданы методы, позволяющие получать пользовательскую информацию

4. Создана модель токена `./auth/db/models/token_models/oauth_token.py`

5. Создается модель пароля и метод, умеющий генерировать валидный пароль `./auth/services/models/signup.py`

6. Создается модель для хранения oauth данных `./auth/db/auth/yandex_oauth.py`

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

- http://localhost:8000/auth/openapi http://localhost:8000/api/openapi если не нужен SSL
- https://localhost/auth/openapi https://localhost/api/openapi если установили сертификаты

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