#!/bin/bash

wait_for_mongo() {
   echo "Waiting for Mongo..."
   while ! nc -z "$MONGO_HOST" "$MONGO_PORT"; do
     sleep 1
   done
   echo "Mongo is ready!"
}

wait_for_kafka() {
   echo "Waiting for Kafka..."
   while ! nc -z "$KAFKA_HOST" "$KAFKA_PORT"; do
     sleep 1
   done
   echo "Kafka is ready!"
}

wait_for_mongo
wait_for_kafka

export PYTHONPATH=$PYTHONPATH:/.
python etl.py