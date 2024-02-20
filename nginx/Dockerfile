FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /var/www/static \
    && mkdir -p /var/www/media \
    && mkdir /etc/nginx/ssl

COPY data/ /var/www/static

COPY ssl/localhost.crt /etc/nginx/ssl/localhost.crt
COPY ssl/localhost.key /etc/nginx/ssl/localhost.key



EXPOSE 80 443