#!/bin/bash

wait_for_kafka() {
   echo "Waiting for Kafka..."
   while ! nc -z "$KAFKA_HOST" "$KAFKA_PORT"; do
     sleep 1
   done
   echo "Kafka is ready!"
}

wait_for_kafka

export PYTHONPATH=$PYTHONPATH:/.
python pywsgi.py