#!/bin/bash
# entrypoint.sh

# Без экспорта pythonpath не импортируются другие модули проекта
export PYTHONPATH=$PYTHONPATH:/.
python3 ./utils/wait_for_es.py
python3 ./utils/wait_for_redis.py
python3 ./testdata/create_indecies.py

exec "$@"
