FROM        azelf/letusgo:base

# Django
COPY        . /srv/dev
RUN         mv /srv/dev/.master /srv/master

RUN         mkdir -p /var/log/gunicorn &&\
            mkdir -p /srv/dev/.log &&\
            mkdir -p /srv/master/.log

RUN         rm -rf  /etc/nginx/sites-available/* &&\
            rm -rf  /etc/nginx/site-enabled/* &&\
            cp -a   /srv/dev/.config/nginx*.conf \
                    /etc/nginx/conf.d/

ENV         DJANGO_SETTINGS_MODULE=config.settings.production_dev
WORKDIR     /srv/dev/app
RUN         python manage.py collectstatic --noinput

ENV         DJANGO_SETTINGS_MODULE=config.settings.production_master
WORKDIR     /srv/master/app
RUN         python manage.py collectstatic --noinput

# CMD
WORKDIR     /srv/dev
CMD         supervisord -c /srv/dev/.config/supervisord.conf -n
EXPOSE      80
