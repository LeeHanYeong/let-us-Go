FROM        azelf/letusgo:base

COPY        . /srv/dev
COPY        .master /srv/master

RUN         mkdir /var/log/gunicorn &&\
            mkdir /srv/dev/.log

RUN         rm -rf  /etc/nginx/sites-available/* &&\
            rm -rf  /etc/nginx/site-enabled/* &&\
            cp -a   /srv/dev/.config/nginx*.conf \
                    /etc/nginx/conf.d/

ENV         DJANGO_SETTINGS_MODULE=config.settings.production_dev
WORKDIR     /srv/dev/app
RUN         python3 manage.py collectstatic --noinput

ENV         DJANGO_SETTINGS_MODULE=config.settings.production_master
WORKDIR     /srv/master/app
RUN         python3 manage.py collectstatic --noinput

WORKDIR     /srv/dev
CMD         supervisord -c /srv/dev/.config/supervisord.conf -n
EXPOSE      80
