FROM        python:3.8-slim
ENV         LANG C.UTF-8

COPY        .config/pgdg.list /tmp/
ADD         https://www.postgresql.org/media/keys/ACCC4CF8.asc /tmp/

RUN         apt -y update &&\
            apt -y install gnupg &&\
            apt-key add /tmp/ACCC4CF8.asc &&\
            apt -y remove gnupg &&\
            apt -y autoremove

RUN         cp /tmp/pgdg.list /etc/apt/sources.list.d/ &&\
            apt -y update &&\
            apt -y dist-upgrade &&\
            apt -y install postgresql-client-12 &&\
            apt -y autoremove

ARG         requirements
ARG         gunicorn
ARG         wsgi
ARG         settings

COPY        $requirements /tmp/$requirements
RUN         pip install -r /tmp/$requirements --no-cache-dir
RUN         mkdir /var/log/gunicorn

COPY        .   /srv/
WORKDIR     /srv/app

ENV         gunicorn ${gunicorn}
ENV         wsgi ${wsgi}
ENV         DJANGO_SETTINGS_MODULE ${settings}

EXPOSE      8000
CMD         python manage.py collectstatic --noinput &&\
            python manage.py migrate --noinput &&\
            gunicorn -c ${gunicorn} ${wsgi}
