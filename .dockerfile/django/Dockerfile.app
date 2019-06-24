FROM azelf/letusgo:base
ENV DJANGO_SETTINGS_MODULE=config.settings.production

COPY ../.. /srv/project
WORKDIR /srv/project/app
CMD python3 manage.py runserver 0:80
