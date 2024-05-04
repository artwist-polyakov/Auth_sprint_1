#!/bin/sh

export RABBIT_MQ_HOST=${RABBIT_MQ_HOST:-"localhost"}
export RABBIT_MQ_PORT=${RABBIT_MQ_PORT:-5672}
export RABBIT_MQ_TASKS_KEY=${RABBIT_MQ_TASKS_KEY:-"_tasks"}
export RABBIT_MQ_NOTIFICATIONS_KEY=${RABBIT_MQ_NOTIFICATIONS_KEY:-"_notifications"}
export RABBIT_MQ_ENRICHED_KEY=${RABBIT_MQ_ENRICHED_KEY:-"_enriched"}
export RABBIT_MQ_TO_SENDING_KEY=${RABBIT_MQ_TO_SENDING_KEY:-"_to_sending"}
export RABBIT_MQ_EXCHANGE=${RABBIT_MQ_EXCHANGE:-"_my_exchange"}
export RABBIT_MQ_TASKS_QUEUE=${RABBIT_MQ_TASKS_QUEUE:-"_TasksQueue"}
export RABBIT_MQ_NOTIFICATIONS_QUEUE=${RABBIT_MQ_NOTIFICATIONS_QUEUE:-"_NotificationsQueue"}
export RABBIT_MQ_ENRICHED_QUEUE=${RABBIT_MQ_ENRICHED_QUEUE:-"_EnrichedQueue"}
export RABBIT_MQ_TO_SENDING_QUEUE=${RABBIT_MQ_TO_SENDING_QUEUE:-"_ToSendingQueue"}

#waiting for rabbitmq-server to start
set -e
until timeout 1 bash -c 'cat < /dev/null > /dev/tcp/${RABBIT_MQ_HOST}/${RABBIT_MQ_PORT}'; do
  >&2 echo "RabbitMQ is unavailable - sleeping"
  sleep 1
done

>&2 echo "RabbitMQ is up - executing command"

#executing command

rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare exchange name=${RABBIT_MQ_EXCHANGE} type=direct

rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare queue name=${RABBIT_MQ_TASKS_QUEUE} durable=true
rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare queue name=${RABBIT_MQ_NOTIFICATIONS_QUEUE} durable=true
rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare queue name=${RABBIT_MQ_ENRICHED_QUEUE} durable=true
rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare queue name=${RABBIT_MQ_TO_SENDING_QUEUE} durable=true

rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare binding source=${RABBIT_MQ_EXCHANGE} destination_type=queue destination=${RABBIT_MQ_TASKS_QUEUE} routing_key=${RABBIT_MQ_TASKS_KEY}
rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare binding source=${RABBIT_MQ_EXCHANGE} destination_type=queue destination=${RABBIT_MQ_NOTIFICATIONS_QUEUE} routing_key=${RABBIT_MQ_NOTIFICATIONS_KEY}
rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare binding source=${RABBIT_MQ_EXCHANGE} destination_type=queue destination=${RABBIT_MQ_ENRICHED_QUEUE} routing_key=${RABBIT_MQ_ENRICHED_KEY}
rabbitmqadmin -H ${RABBIT_MQ_HOST} -P ${RABBIT_MQ_PORT} declare binding source=${RABBIT_MQ_EXCHANGE} destination_type=queue destination=${RABBIT_MQ_TO_SENDING_QUEUE} routing_key=${RABBIT_MQ_TO_SENDING_KEY}


echo "Initialization completed"