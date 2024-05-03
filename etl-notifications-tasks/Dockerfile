FROM python:3.10-alpine

WORKDIR /app

COPY ./etl.py /app/etl.py
COPY ./mycron /app/mycron
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && crontab mycron

CMD crond -f && tail -f /logs/logs.log