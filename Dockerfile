FROM        azelf/letusgo:base
ENV         DJANGO_SETTINGS_MODULE=config.settings.production

COPY        . /srv/project

RUN         rm -rf  /etc/nginx/sites-available/* &&\
            rm -rf  /etc/nginx/site-enabled/* &&\
            cp -a   /srv/project/.config/nginx*.conf \
                    /etc/nginx/conf.d/

RUN         cp -f   /srv/project/.config/supervisord.conf \
                    /etc/supervisor/conf.d/

WORKDIR     /srv/project/app
EXPOSE      80
RUN         python3 manage.py collectstatic --noinput
CMD         supervisord -n
