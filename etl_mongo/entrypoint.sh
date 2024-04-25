#!/bin/bash

wait_for_mongo() {
     # Ожидаем доступности сервера MongoDB на заданном хосте и порту
     local host=$1
     local port=27017
     echo "Waiting for MongoDB at $host on port $port..."
     while ! nc -z $host $port; do
         sleep 1
     done
     echo "MongoDB at $host on port $port is up and running."
 }

wait_for_kafka() {
   echo "Waiting for Kafka..."
   while ! nc -z "$KAFKA_HOST" "$KAFKA_PORT"; do
     sleep 1
   done
   echo "Kafka is ready!"
}

wait_for_mongo mongo1
wait_for_mongo mongo2
wait_for_mongo mongo3
wait_for_kafka

export PYTHONPATH=$PYTHONPATH:/.
python etl.py