FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY denied.html /usr/share/nginx/html/denied.html
COPY ru-aggregated.zone /tmp/ru-aggregated.zone

RUN awk '{print $1 " 1;"}' /tmp/ru-aggregated.zone > /etc/nginx/ru-prefixes.conf \
    && rm /tmp/ru-aggregated.zone

EXPOSE 80
