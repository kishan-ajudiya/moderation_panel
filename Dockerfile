FROM python:3-alpine

ENV PYTHONUNBUFFERED 1

RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
                mariadb-dev \
                python3-dev \
                mysql-client \
                nginx \
                openrc \
        ;
#RUN apk update && apk add py-mysqldb && apk add mysql-client
RUN mkdir /moderation_panel

WORKDIR /moderation_panel

COPY requirements.txt /moderation_panel/

RUN pip install -r requirements.txt

RUN touch /etc/nginx/conf.d/moderation_panel.conf

COPY . /moderation_panel/

COPY docker_config/nginx/moderation_panel.conf /etc/nginx/conf.d/moderation_panel.conf

RUN mkdir /moderation_panel/logs && mkdir /moderation_panel/static && /run/nginx/ &&  mkdir /run/openrc/ && touch /run/nginx/nginx.pid && touch /run/openrc/softlevel

EXPOSE 80
EXPOSE 3308
EXPOSE 3003
EXPOSE 8000
EXPOSE 8095