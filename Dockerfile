# syntax = docker/dockerfile:experimental
FROM        python:3.10-slim

# Language, Timezone
ENV         LANG C.UTF-8
ENV         TZ Asia/Seoul
RUN         ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN         apt -y update &&\
            apt -y dist-upgrade &&\
            apt -y autoremove

# requirements
ARG         requirements
COPY        $requirements /tmp/$requirements

RUN         --mount=type=cache,target=/root/.cache/pip \
            pip install -r /tmp/$requirements

ARG         wsgi
ENV         wsgi ${wsgi}
ARG         gunicorn
ENV         gunicorn ${gunicorn}
ARG         settings
ENV         DJANGO_SETTINGS_MODULE ${settings}

# Log folders
RUN         mkdir /var/log/gunicorn
RUN         mkdir /var/log/celery

# Copy sources
COPY        .   /srv/
WORKDIR     /srv/app

EXPOSE      8000
CMD         python manage.py collectstatic --noinput &&\
            python manage.py migrate --noinput &&\
            gunicorn -c ${gunicorn} ${wsgi}
