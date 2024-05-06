FROM python:3.10-alpine
RUN apk update && apk add --no-cache supervisor


WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY fake_sendmail /usr/local/bin/fake_sendmail
RUN chmod +x /usr/local/bin/fake_sendmail


COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY . /app/

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]