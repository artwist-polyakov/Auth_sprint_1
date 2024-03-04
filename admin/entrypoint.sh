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

python manage.py migrate

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL"
fi

python manage.py runserver "$ADMIN_HOST":"$ADMIN_PORT"