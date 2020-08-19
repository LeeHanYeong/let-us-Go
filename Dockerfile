FROM        python:3.8-slim
ENV         LANG C.UTF-8
RUN         apt -y update &&\
            apt -y dist-upgrade

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

CMD         python manage.py collectstatic --noinput &&\
            python manage.py migrate --noinput &&\
            gunicorn -c ${gunicorn} ${wsgi}
