FROM        azelf/letusgo:base

COPY        . /srv/dev
RUN         mkdir /srv/master &&\
            mkdir /var/log/gunicorn
RUN         tar -xzvf /srv/dev/master.tar -C /srv/master

COPY        .secrets /srv/master/.secrets

RUN         rm -rf  /etc/nginx/sites-available/* &&\
            rm -rf  /etc/nginx/site-enabled/* &&\
            cp -a   /srv/dev/.config/nginx*.conf \
                    /etc/nginx/conf.d/

WORKDIR     /srv/dev/app
RUN         DJANGO_SETTINGS_MODULE=config.settings.production_dev python3 manage.py collectstatic --noinput
#RUN         DJANGO_SETTINGS_MODULE=config.settings.production_dev python3 manage.py migrate --noinput

ENV         DJANGO_SETTINGS_MODULE=config.settings.production_master
WORKDIR     /srv/master/app
RUN         python3 manage.py collectstatic --noinput
#RUN         python3 manage.py migrate --noinput


WORKDIR     /srv/dev
CMD         supervisord -c /srv/dev/.config/supervisord.conf -n
EXPOSE      80
