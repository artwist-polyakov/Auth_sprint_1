#!/bin/bash

export RABBIT_MQ_HOST=${RABBIT_MQ_HOST:-"localhost"}
export RABBIT_MQ_PORT=${RABBIT_MQ_PORT:-5672}

#waiting for rabbitmq-server to start
set -e
until timeout 1 bash -c 'cat < /dev/null > /dev/tcp/${RABBIT_MQ_HOST}/${RABBIT_MQ_PORT}'; do
  >&2 echo "RabbitMQ is unavailable - sleeping"
  sleep 1
done
echo "RabbitMQ is up - executing command"
echo "##################################"
