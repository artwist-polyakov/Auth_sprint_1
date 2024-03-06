#!/bin/bash

wait_for_postgres() {
   echo "Waiting for Postgres..."
   while ! nc -z postgres "$POSTGRES_PORT"; do
     sleep 1
   done
   echo "Postgres is ready!"
}

wait_for_jaeger() {
   echo "Waiting for Jaeger..."
   while ! nc -z jaeger "$JAEGER_PORT"; do
     sleep 1
   done
   echo "Jaeger is ready!"
}

wait_for_postgres
wait_for_jaeger

export PYTHONPATH=$PYTHONPATH:/.
# команда: alembic upgrade head
# для вывода логов:
alembic upgrade head 2>&1 | tee alembic.log

uvicorn main:app --proxy-headers --host "$AUTH_HOST" --port "$AUTH_PORT"