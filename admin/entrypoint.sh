#!/bin/bash

wait_for_postgres() {
   echo "Waiting for Postgres..."
   while ! nc -z postgres "$POSTGRES_PORT"; do
     sleep 1
   done
   echo "Postgres is ready!"
}

wait_for_postgres

python manage.py collectstatic

python manage.py makemigrations
python manage.py migrate --fake-initial

python manage.py runserver "$ADMIN_HOST":"$ADMIN_PORT"