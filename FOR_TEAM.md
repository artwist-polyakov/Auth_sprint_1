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


## Ручное применение существующих миграций

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
```shell
cd ./auth/
alembic revision --autogenerate
```

`--autogenerate` обеспечивает сравнение моделей в коде и состояния базы данных

_Внимание_. На всем пути работы `alembic` не должно быть импортов settings (включая файлы с моделями `./auth/db/auth`). 
Это связано с тем, что скрипт alembic не сможет прочитать .env, который находится в корне проекта `cd .`

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
_Внимание_. Чтобы избежать ошибки DuplicateObjectError, необходимо заполнять не только `def upgrade()`, но и `def downgrade()` (запрос `DELETE`)