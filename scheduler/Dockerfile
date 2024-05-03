FROM ubuntu:16.04

ARG RABBIT_MQ_HOST
ARG RABBIT_MQ_PORT

WORKDIR .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get install -y netcat-openbsd gettext cron rsyslog\
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN crontab /core/mycron
CMD crond -f && tail -f /logs/logs.log

RUN ["chmod", "+x", "entrypoint.sh"]
ENTRYPOINT ["./entrypoint.sh"]
