#!/bin/bash

wait_for_postgres() {
   echo "Waiting for Postgres..."
   while ! nc -z postgres $POSTGRES_PORT; do
     sleep 1
   done
   echo "Postgres is ready!"
}

uvicorn main:app --proxy-headers --host $AUTH_HOST --port $AUTH_PORT