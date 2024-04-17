# Шаги по запуску тестов

## Предварительная установка

```shell
cd ./research
pip install -r ./requirements.txt

git clone https://github.com/mongodb/mongo-python-driver.git pymongo
cd pymongo/
pip install .

```

## Запуск контейнеров

```shell
cd ./research
docker-compose up --build

```

## Подготовка mongo

Заходим в контейнер

```shell
docker exec -it mongodb mongosh
```

Создаем БД

```shell
use TestDB
```


## ПРОВЕДЕНИЕ ТЕСТОВ


```shell
cd ./research
python main.py

```
