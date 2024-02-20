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

## Первая версия функциональных тестов

потребуется библиотека requests
```shell
pip install requests
```

запуск тестов
```shell
python tests_simple/test_es_query.py    
```

## Генерация собственного сертификата

```shell
openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -nodes \
   -keyout localhost.key -out localhost.crt -subj "/CN=localhost" \
   -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```
