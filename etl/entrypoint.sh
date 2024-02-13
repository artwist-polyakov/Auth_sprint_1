#!/bin/bash

wait_for_postgres() {
   echo "Waiting for Postgres..."
   while ! nc -z postgres $POSTGRES_PORT; do
     sleep 1
   done
   echo "Postgres is ready!"
}

wait_for_elastic_node_1() {
  tries=1
  echo "Waiting for Elastisearch node 1..."
  until curl "elasticsearch-node1:$ELASTIC_PORT/_cluster/health?wait_for_status=yellow&timeout=30s"; do
    >&2 echo "Elastisearch is unavailable - waiting for it... 😴 ($tries)"
    sleep 1
    tries=$(expr $tries + 1)
  done
  echo "Elasticsearch node 1 is ready!"
}

wait_for_elastic_node_2() {
  tries=1
  echo "Waiting for Elastisearch node 2..."
  until curl "elasticsearch-node2:$ELASTIC_PORT/_cluster/health?wait_for_status=yellow&timeout=30s"; do
    >&2 echo "Elastisearch is unavailable - waiting for it... 😴 ($tries)"
    sleep 1
    tries=$(expr $tries + 1)
  done
  echo "Elasticsearch node 2 is ready!"
}

wait_for_redis() {
   echo "Waiting for Redis..."
   while ! nc -z redis $REDIS_PORT; do
     sleep 1
   done
   echo "Redis is ready!"
}


wait_for_postgres
wait_for_elastic_node_1
wait_for_elastic_node_2
wait_for_redis

echo "All containers are ready"

# Без экспорта pythonpath db/load_data.py не может импортировать другие модули
export PYTHONPATH=$PYTHONPATH:/.
python load_data_to_postgres.py

echo "Ready to start etl"
python etl.py
