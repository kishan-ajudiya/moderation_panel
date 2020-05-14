FROM python:3.8.2-alpine3.11

MAINTAINER Kishan Ajudiya <kishan.ajudiya@go-mmt.com>

ARG env
ENV CURR_ENV=$env

RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
                mariadb-dev \
                python3-dev \
                mysql-client \
                nginx \
                supervisor \
                openrc \
        ;
#RUN apk update && apk add py-mysqldb && apk add mysql-client
RUN mkdir /moderation_panel

WORKDIR /moderation_panel

COPY requirements.txt /moderation_panel/

RUN pip install -r requirements.txt

RUN touch /etc/nginx/conf.d/moderation_panel.conf

COPY . /moderation_panel/



COPY docker_config/supervisord/supervisord /etc/init.d/supervisord
COPY docker_config/supervisord/moderation_panel.ini /etc/supervisord.d/
COPY docker_config/supervisord/supervisord.conf /etc/supervisord.conf

RUN chmod 755 /etc/init.d/supervisord


COPY docker_config/nginx/nginx.conf /etc/nginx/nginx.conf
COPY docker_config/nginx/moderation_panel.conf /etc/nginx/conf.d/moderation_panel.conf
RUN rm -rf /etc/nginx/conf.d/default.conf

RUN mkdir  mkdir /moderation_panel/static && mkdir /run/nginx/ &&  mkdir /run/openrc/ && touch /run/nginx/nginx.pid && touch /run/openrc/softlevel 

RUN echo yes | python manage.py collectstatic

EXPOSE 80
EXPOSE 8000

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisord.d/moderation_panel.ini"]


