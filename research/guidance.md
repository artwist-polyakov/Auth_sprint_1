# Шаги по запуску тестов

## 1) Предварительная установка

```shell
cd ./research
pip install -r ./requirements.txt

git clone https://github.com/mongodb/mongo-python-driver.git pymongo
cd pymongo/
pip install .

```

## 2) Запуск контейнеров

```shell
cd ./research
docker-compose up --build

```

## 3) Подготовка mongo

Заходим в контейнер

```shell
docker exec -it mongodb mongosh
```

Создаем БД

```shell
use TestDB
```


## 4) ПРОВЕДЕНИЕ ТЕСТОВ


```shell
cd ./research
python main.py

```
