# syntax = docker/dockerfile:experimental
# Dockerfile로 단독실행되지 않으며, 반드시 .deploy/ 내의 docker-compose.yml을 사용한 docker-compose로 실행
FROM        python:3.8-slim

# Language, Timezone
ENV         LANG C.UTF-8
ENV         TZ Asia/Seoul
RUN         ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY        .deploy/pgdg.list /tmp/
ADD         https://www.postgresql.org/media/keys/ACCC4CF8.asc /tmp/

RUN         --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
            apt -y update &&\
            apt -y install gnupg &&\
            apt-key add /tmp/ACCC4CF8.asc &&\
            apt -y remove gnupg &&\
            # Pillow
            apt -y autoremove

RUN         cp /tmp/pgdg.list /etc/apt/sources.list.d/ &&\
            apt -y update &&\
            apt -y dist-upgrade &&\
            apt -y install postgresql-client-13 &&\
            apt -y autoremove

# requirements
ARG         requirements
COPY        $requirements /tmp/$requirements

RUN         --mount=type=cache,target=/root/.cache/pip \
            pip install supervisor &&\
            pip install -r /tmp/$requirements

ARG         wsgi
ENV         wsgi ${wsgi}
ARG         gunicorn
ENV         gunicorn ${gunicorn}
ARG         settings
ENV         DJANGO_SETTINGS_MODULE ${settings}

# Log folders
RUN         mkdir /var/log/gunicorn &&\
            mkdir /var/log/celery

# Copy sources
COPY        .   /srv/
WORKDIR     /srv/app

EXPOSE      8000
CMD         python manage.py collectstatic --noinput &&\
            python manage.py migrate --noinput &&\
            gunicorn -c ${gunicorn} ${wsgi}
