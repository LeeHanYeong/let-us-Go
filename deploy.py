#!/usr/bin/env python
import json
import os
import subprocess

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')
SECRETS = json.load(open(os.path.join(SECRETS_DIR, 'base.json')))

ACCESS_KEY = SECRETS['AWS_EB_ACCESS_KEY_ID']
SECRET_KEY = SECRETS['AWS_EB_SECRET_ACCESS_KEY']
ENV = dict(os.environ, AWS_ACCESS_KEY_ID=ACCESS_KEY, AWS_SECRET_ACCESS_KEY=SECRET_KEY)


def run(cmd):
    subprocess.run(cmd, shell=True, env=ENV)


run('docker build -t azelf/letusgo:base -f .dockerfile/django/Dockerfile.base .')
run('docker build -t azelf/letusgo:nginx -f .dockerfile/nginx/Dockerfile .dockerfile/nginx')
run('docker push azelf/letusgo:base')
run('docker push azelf/letusgo:nginx')

run('container-transform --input-type compose --output-type ecs docker-compose.yml > Dockerrun.aws.json')
run('docker build -t letusgo:django -f .dockerfile/django/Dockerfile.django .')
run('docker tag letusgo:django 347809506342.dkr.ecr.ap-northeast-2.amazonaws.com/letusgo:django')
run('$(aws ecr get-login --no-include-email --region ap-northeast-2) && '
    'docker push 347809506342.dkr.ecr.ap-northeast-2.amazonaws.com/letusgo:django')
run('eb deploy --staged')

# subprocess.run('docker build -t letusgo:app -f .dockerfile/django/Dockerfile.app .', shell=True)
# subprocess.run('python app/manage.py collectstatic --noinput', shell=True)
# subprocess.run('git add -f .secrets/'.split(), shell=True)
# subprocess.run('git add -f .static/'.split(), shell=True)
# subprocess.run('eb deploy --staged &'.split(), shell=True)
# subprocess.run('sleep 7'.split(), shell=True)
# subprocess.run('git reset HEAD .secrets/'.split(), shell=True)
# subprocess.run('git reset HEAD .static/'.split(), shell=True)
