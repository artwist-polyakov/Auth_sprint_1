#!/bin/bash

wait_for_postgres() {
   echo "Waiting for Postgres..."
   while ! nc -z "$NOTIFICATIONS_DB_HOST" "$NOTIFICATIONS_DB_PORT"; do
     sleep 1
   done
   echo "Postgres is ready!"
}

wait_for_postgres

export PYTHONPATH=$PYTHONPATH:/.
# команда: alembic upgrade head
# для вывода логов:
alembic upgrade head 2>&1 | tee alembic.log

uvicorn main:app --proxy-headers --host $NOTIFICATIONS_HOST --port $NOTIFICATIONS_PORT