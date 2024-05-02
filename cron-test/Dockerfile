FROM python:3.10-alpine
COPY ./test.py /app/test.py
COPY ./mycron /app/mycron
RUN crontab /app/mycron
CMD crond -f && tail -f /logs/logs.log