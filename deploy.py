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

subprocess.run('docker build -t azelf/letusgo:base -f .dockerfile/django/Dockerfile.base .', shell=True)
subprocess.run('docker push azelf/letusgo:base', shell=True)
subprocess.run('docker build -t letusgo .', shell=True)
subprocess.run('python app/manage.py collectstatic --noinput', shell=True)
# subprocess.run('git add -f .secrets/'.split(), shell=True)
# subprocess.run('git add -f .static/'.split(), shell=True)
# subprocess.run('eb deploy --staged &'.split(), shell=True)
# subprocess.run('sleep 7'.split(), shell=True)
# subprocess.run('git reset HEAD .secrets/'.split(), shell=True)
# subprocess.run('git reset HEAD .static/'.split(), shell=True)
