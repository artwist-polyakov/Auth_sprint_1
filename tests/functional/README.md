## Подготовка к тестированию

### Запустить docker-compose тестов

```commandline
docker-compose -f ./tests/functional/docker-compose.yml up -d --build
```

или

```commandline
cd tests/functional
docker-compose up -d --build
```

### Посмотреть логи тестов

```commandline
 docker-compose -f ./tests/functional/docker-compose.yml  logs tests 
```

или

```commandline  
cd tests/functional
docker-compose logs tests
```


### Остановить контейнеры тестов

```commandline
docker-compose -f ./tests/functional/docker-compose.yml down -v
```

или 

```commandline
cd tests/functional
docker-compose down -v
```