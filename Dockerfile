FROM        azelf/letusgo:base

COPY        . /srv/dev
WORKDIR     /srv/dev
RUN         tar -xzvf master.zip -C /srv/master

COPY        .secrets /srv/master

RUN         rm -rf  /etc/nginx/sites-available/* &&\
            rm -rf  /etc/nginx/site-enabled/* &&\
            cp -a   /srv/dev/.config/nginx*.conf \
                    /etc/nginx/conf.d/

RUN         cp -f   /srv/dev/.config/supervisord.conf \
                    /etc/supervisor/conf.d/

ENV         DJANGO_SETTINGS_MODULE=config.settings.production_dev
WORKDIR     /srv/dev/app
RUN         python3 manage.py collectstatic --noinput
RUN         python3 manage.py migrate --noinput

ENV         DJANGO_SETTINGS_MODULE=config.settings.production_master
WORKDIR     /srv/master/app
RUN         python3 manage.py collectstatic --noinput
RUN         python3 manage.py migrate --noinput

EXPOSE      80
CMD         supervisord -n
