FROM python:3.10-alpine
COPY ./etl.py /app/etl.py
COPY ./mycron /app/mycron
RUN crontab /app/mycron
CMD crond -f && tail -f /logs/logs.log