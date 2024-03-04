#!/bin/bash

wait_for_postgres() {
   echo "Waiting for Postgres..."
   while ! nc -z postgres $POSTGRES_PORT; do
     sleep 1
   done
   echo "Postgres is ready!"
}

wait_for_postgres

python manage.py migrate
python manage.py runserver