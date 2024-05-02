ARG RABBIT_MQ_VERSION

FROM rabbitmq:${RABBIT_MQ_VERSION}-alpine

# Копирование скрипта init.sh в папку /rabbitmq внутри контейнера
COPY init.sh /rabbitmq/init.sh

# Даем права на выполнение
RUN chmod +x /rabbitmq/init.sh