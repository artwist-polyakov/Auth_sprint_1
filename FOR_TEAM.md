# О продукте

## Описание

Веб-приложение онлайн-кинотеатр.
![Главный экран](https://pictures.s3.yandex.net/resources/00_welcome_content_images_S1_1_Practix_1603713438.jpg)

В настоящий момент реализована только часть функционала.
Приложение импортирует данные в PostgresSQL и ElasticSearch и предоставляет API для получения данных.

## Стек технологий

- Python 3.10
- FastAPI
- PostgreSQL
- ElasticSearch
- Docker
- Docker-compose
- Nginx
- Redis
- Uvicorn

# Правила работы с репозиторием

## Принцип ведения репозитория

Git-flow

Все изменения в dev ветку репозитория вносятся через пулл-реквесты.
Каждое изменения должно быть подтверждено минимум одним ревьюером.

## Ветки

Рабочие ветки в репозитории называются по следующему шаблону:
- `feature/<номер-связанной-задачи>-<название-фичи>` - ветка для разработки новой фичи
- `bugfix/<номер-связанной-задачи>-<название-фикса>` - ветка для исправления багов

## Коммиты

Коммиты в репозитории называются по следующему шаблону:

 `<что делает коммит>`


# Проверка кода

Перед выкладкой кода в репозиторий необходимо проверить код на соответствие стандартам.

## Подключение линтеров

```shell
pip install flake8
pip install isort
```

## Запуск линтеров

Запуск flake8
```shell
flake8 --config=.flake8
```

Запуск isort
```shell
isort .
```

## Функциональные тесты

Инструкция по запуску тестов в отдельном контейнере:

```shell
cd ./tests/functional
README.md
```

## Генерация собственного сертификата

1. Создать корневой сертификат

Лично я заменяю `RootCA` на `PoliakovCA` чтобы отличать свои сертификаты от других.

```shell
openssl req -x509 -nodes -new -sha256 -days 1024 -newkey rsa:2048 -keyout RootCA.key -out RootCA.pem -subj "/C=US/CN=Example-Root-CA"
openssl x509 -outform pem -in RootCA.pem -out RootCA.crt
```

2. Конфигурируем файл `domains.ext` в корне проекта

3. Запускаем в корне проекта команду

```shell

openssl req -new -nodes -newkey rsa:2048 -keyout localhost.key -out localhost.csr -subj "/C=US/ST=YourState/L=YourCity/O=Example-Certificates/CN=localhost.local"
openssl x509 -req -sha256 -days 1024 -in localhost.csr -CA RootCA.pem -CAkey RootCA.key -CAcreateserial -extfile domains.ext -out localhost.crt

```

4. Копируем созданные сертификаты `localhost.crt` и `localhost.key` в папку `./nginx/ssl`
5. Делаем сертификат `RootCA.crt` доверенным в браузере


## Применение миграций сервиса UGC (Clickhouse)
```clickhouse-migrations --db-host localhost --migrations-dir ./migrations```


## Ручное применение существующих миграций сервиса авторизации

На данный момент миграции выполняются автоматически. При необходимости можно сделать это вручную:

1. Установить библиотеку:
```shell
pip install alembic==1.13.1
```
2. Если требуется, поменять роли по умолчанию в файле `cd ./auth/migrations/roles/default_roles.py`

3. В `./auth/migrations/.env` поменять хост на localhost

4. Применить миграции (контейнеры запускать не нужно):
```shell
cd ./auth/
alembic upgrade head
```

## Инструкция по работе с миграциями (alembic)

1. Установка библиотеки:
```shell
pip install alembic==1.13.1
```

Если в сервисе отсутствуют файлы для работы с alembic:
- выполните команды:
```shell
cd ./auth/
alembic init migrations
```
- настройте `alembic.ini` и `env.py`.

2. Создание миграции:

РАСКОММЕНТИРУЙТЕ СТРОКИ ИМПОРТОВ В ФАЙЛЕ env.py

```shell
cd ./auth/
alembic revision --autogenerate
```

`--autogenerate` обеспечивает сравнение моделей в коде и состояния базы данных

Чтобы добавить постфикс к имени миграции, добавьте `-m`:
```shell
alembic revision --autogenerate -m "migration_name"
```

3. Применить все миграции из `./auth/migrations/versions/` к базе данных
```shell
alembic upgrade head
```
Чтобы применить все миграции до конкретной миграции, нужно указать ее название
```shell
alembic upgrade <revision_name>
```

4. Откатить все миграции
```shell
alembic downgrade base
```
Чтобы откатиться до какой-то миграции, необходимо использовать ее `revision`
```shell
alembic downgrade <revision_name>
```

5. Создать пользовательскую миграцию (миграция для редактирования)
```shell
alembic revision
```

##  Решение некоторых ошибок при работе с миграциями (alembic)

1. Если миграции запускаются из контейнера, в файле `./auth/migrations/.env` должно быть указано имя контейнера, иначе - имя локального хоста (например, `localhost`)

2. На всем пути работы `alembic` не должно быть импортов `./auth/configs/settings.py` (включая файлы с моделями `./auth/db/auth`).
Это связано с тем, что скрипт `alembic` не сможет прочитать `.env`, который находится в корне проекта `cd .`

3. Если возвращается ошибка `Foreign key couldn't find column` или `print ...`, необходимо прописать импорты моделей из `./auth/db/auth` в `./auth/migrations/env.py`; импорта `Base`, от которого наследуются другие модели, недостаточно

4. Чтобы избежать ошибки `DuplicateObjectError`, необходимо заполнять не только `def upgrade()`, но и `def downgrade()` (запрос `DELETE/DROP`)

5. При создании миграции модели, содержащей `UniqueConstraint` (например, `UserSignIn`), необходимо удалить из файла миграции строку `sa.UniqueConstraint('uuid')` (генерируется автоматически для всех таблиц с `PK uuid`). Иначе возникает ошибка:
```shell
 sqlalchemy.exc.DBAPIError: (sqlalchemy.dialects.postgresql.asyncpg.Error)
 <class 'asyncpg.exceptions.FeatureNotSupportedError'>: unique constraint on partitioned table must include all partitioning columns
 DETAIL:  UNIQUE constraint on table "user_sign_ins" lacks column "user_device_type" which is part of the partition key.
```
Это связано с тем, что при создании `UniqueConstraint` необходимо указать и `uuid`, и `user_device_type`, и строка `sa.UniqueConstraint('uuid')` вызывает ошибку даже если есть вторая правильная строка c `UniqueConstraint`, которая генерируется из модели

6. Иногда могут быть ошибки при работе с действующим venv проекта, в таком случае очистите виртуальное окружение.

```shell

cd ..
pip freeze | xargs pip uninstall -y
cd ./auth/
pip install -r requirements.txt

```

## Полезные команды

1. Генератор UUID4
```shell

docker exec -it auth python utils/uuid_generator.py

```


Как подключиться к ClickHouse через консоль.
```shell

docker exec -it clickhouse-node1 bash

```

как админ
```shell

clickhouse-client -u admin --password 123 -d default

```


как дата аналитик
```shell

clickhouse-client -u data_analyst --password data_analyst_pass -d default

```

Как подключиться к ClickHouse через DBeaver


как админ
```shell

host = localhost
port = 8123
db = movies
login = data_analyst
password = data_analyst_pass

```


как дата аналитик
```shell

host = localhost
port = 8123
login = admin
password = 123

```
