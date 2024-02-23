#!/bin/bash
# entrypoint.sh

wait_for_postgres() {
   echo "Waiting for Postgres..."
   while ! nc -z postgres "$POSTGRES_PORT"; do
     sleep 1
   done
   echo "Postgres is ready!"
}

# Без экспорта pythonpath не импортируются другие модули проекта
export PYTHONPATH=$PYTHONPATH:/.
python3 ./utils/wait_for_es.py
python3 ./utils/wait_for_redis.py
python3 ./testdata/create_indecies.py

exec "$@"
