#!/bin/sh

export RABBIT_MQ_HOST=${RABBIT_MQ_HOST:-"localhost"}
export RABBIT_MQ_PORT=${RABBIT_MQ_PORT:-5672}
export RABBIT_MQ_TASKS_KEY=${RABBIT_MQ_TASKS_KEY:-"tasks"}
export RABBIT_MQ_NOTIFICATIONS_KEY=${RABBIT_MQ_NOTIFICATIONS_KEY:-"notifications"}
export RABBIT_MQ_ENRICHED_KEY=${RABBIT_MQ_ENRICHED_KEY:-"enriched"}
export RABBIT_MQ_TO_SENDING_KEY=${RABBIT_MQ_TO_SENDING_KEY:-"to_sending"}

#waiting for rabbitmq-server to start
set -e
until timeout 1 bash -c 'cat < /dev/null > /dev/tcp/${RABBIT_MQ_HOST}/${RABBIT_MQ_PORT}'; do
  >&2 echo "RabbitMQ is unavailable - sleeping"
  sleep 1
done

>&2 echo "RabbitMQ is up - executing command"

#executing command

rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare exchange name=my_exchange type=direct

rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare queue name=TasksQueue durable=true
rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare queue name=NotificationsQueue durable=true
rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare queue name=EnrichedQueue durable=true
rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare queue name=ToSendingQueue durable=true

rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare binding source=my_exchange destination_type=queue destination=TasksQueue routing_key=${RABBIT_MQ_TASKS_KEY}
rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare binding source=my_exchange destination_type=queue destination=NotificationsQueue routing_key=${RABBIT_MQ_NOTIFICATIONS_KEY}
rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare binding source=my_exchange destination_type=queue destination=EnrichedQueue routing_key=${RABBIT_MQ_ENRICHED_KEY}
rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare binding source=my_exchange destination_type=queue destination=ToSendingQueue routing_key=${RABBIT_MQ_TO_SENDING_KEY}


echo "Initialization completed"