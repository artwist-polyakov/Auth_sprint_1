FROM python:3.10-alpine

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && crontab mycron

CMD crond -f && tail -f /logs/logs.log