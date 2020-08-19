FROM        python:3.8-slim
ENV         LANG C.UTF-8
RUN         apt -y update &&\
            apt -y dist-upgrade

COPY        requirements.txt /tmp/requirements.txt
RUN         pip install -r /tmp/requirements.txt
RUN         mkdir /var/log/gunicorn

COPY        .   /srv/
WORKDIR     /srv/app

CMD         python manage.py collectstatic --noinput && \
            gunicorn -c /srv/.config/gunicorn_dev.py config.wsgi.production_dev
