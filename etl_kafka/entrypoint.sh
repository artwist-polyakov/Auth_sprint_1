#!/bin/bash

wait_for_clickhouse() {
   echo "Waiting for ClickHouse..."
   while ! nc -z "$CLICKHOUSE_HOST" "$CLICKHOUSE_PORT"; do
     sleep 1
   done
   echo "ClickHouse is ready!"
}

wait_for_kafka() {
   echo "Waiting for Kafka..."
   while ! nc -z "$KAFKA_HOST" "$KAFKA_PORT"; do
     sleep 1
   done
   echo "Kafka is ready!"
}

wait_for_clickhouse
wait_for_kafka

export PYTHONPATH=$PYTHONPATH:/.
python etl.py