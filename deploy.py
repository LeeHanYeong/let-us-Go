#!/usr/bin/env python
import argparse
import json
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--build', action='store_true')
parser.add_argument('--run', action='store_true')
args = parser.parse_args()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')
SECRETS = json.load(open(os.path.join(SECRETS_DIR, 'base.json')))

ACCESS_KEY = SECRETS['AWS_EB_ACCESS_KEY_ID']
SECRET_KEY = SECRETS['AWS_EB_SECRET_ACCESS_KEY']
ENV = dict(os.environ, AWS_ACCESS_KEY_ID=ACCESS_KEY, AWS_SECRET_ACCESS_KEY=SECRET_KEY)


def run(cmd, **kwargs):
    subprocess.run(cmd, shell=True, env=ENV, **kwargs)


if __name__ == '__main__':
    run('docker build -t azelf/letusgo:base -f .dockerfile/Dockerfile.base .')
    run('docker push azelf/letusgo:base')
    if args.build:
        exit(0)

    run('python app/manage.py collectstatic --noinput')
    if args.run:
        run('docker build -t letusgo .')
        run('docker run --rm -it -p 8000:80 letusgo')
        exit(0)

    run('git add -A')
    run('git add -f .secrets/')
    run('git add -f .static/')
    run('eb deploy --staged &')
    run('sleep 7')
    run('git reset HEAD', stdout=subprocess.DEVNULL)