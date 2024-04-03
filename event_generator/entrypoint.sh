#!/bin/bash

wait_for_postgres() {
   echo "Waiting for Postgres..."
   while ! nc -z postgres "$POSTGRES_PORT"; do
     sleep 1
   done
   echo "Postgres is ready!"
}

wait_for_kafka() {
   echo "Waiting for Kafka..."
   while ! nc -z "$KAFKA_HOST" "$KAFKA_PORT"; do
     sleep 1
   done
   echo "Kafka is ready!"
}

wait_for_postgres
wait_for_kafka

export PYTHONPATH=$PYTHONPATH:/.
python main.py