FROM        python:3.8-slim
ENV         LANG C.UTF-8
RUN         apt -y update &&\
            apt -y dist-upgrade

COPY        requirements.txt /tmp/
RUN         pip install -r /tmp/requirements.txt

COPY        .   /srv/
