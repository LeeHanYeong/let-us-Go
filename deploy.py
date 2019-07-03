#!/usr/bin/env python
import argparse
import json
import os
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('env')
parser.add_argument('--build', action='store_true')
parser.add_argument('--run', action='store_true')
parser.add_argument('--bash', action='store_true')
args = parser.parse_args()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')
SECRETS = json.load(open(os.path.join(SECRETS_DIR, 'base.json')))

ACCESS_KEY = SECRETS['AWS_EB_ACCESS_KEY_ID']
SECRET_KEY = SECRETS['AWS_EB_SECRET_ACCESS_KEY']
ENV = dict(os.environ, AWS_ACCESS_KEY_ID=ACCESS_KEY, AWS_SECRET_ACCESS_KEY=SECRET_KEY)
ENV['PYTHONPATH'] = ENV.get('PYENV_VIRTUAL_ENV') or ENV.get('VIRTUAL_ENV')


def run(cmd, **kwargs):
    subprocess.run(cmd, shell=True, env=ENV, **kwargs)


if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT_DIR, '.temp'), exist_ok=True)

    # Clone Front Project
    FRONT_DIR = os.path.join(ROOT_DIR, '.front')
    if os.path.exists(FRONT_DIR):
        os.chdir(FRONT_DIR)
        run('git pull')
    else:
        run('git clone git@github.com:Yuni-Q/proj2.git .front')
    os.chdir(ROOT_DIR)

    # curl Node.js install script
    run('curl -sL https://deb.nodesource.com/setup_10.x > .temp/install_node.sh')

    # Build BaseImage
    run('docker pull python:3.7-slim')
    run('docker pull node:lts-slim')
    run('docker build -t azelf/letusgo:base -f .dockerfile/Dockerfile.base .')

    # master코드 분리
    run('rm -rf .master')
    os.makedirs(os.path.join(ROOT_DIR, '.master'), exist_ok=True)
    run('git archive --format=tar.gz master -o ./.master.tar')
    run('tar -xzf .master.tar -C ./.master')
    os.remove(os.path.join(ROOT_DIR, '.master.tar'))
    master_secret_dir = os.path.join(ROOT_DIR, '.master', '.secrets')
    shutil.rmtree(master_secret_dir, ignore_errors=True)
    shutil.copytree(SECRETS_DIR, master_secret_dir)

    # migrate
    run('DJANGO_SETTINGS_MODULE=config.settings.production_dev python app/manage.py migrate --noinput')
    os.chdir(os.path.join(ROOT_DIR, '.master'))
    run('DJANGO_SETTINGS_MODULE=config.settings.production_master python app/manage.py migrate --noinput')
    os.chdir(os.path.join(ROOT_DIR))

    if args.build or args.run or args.bash:
        run('docker build -t letusgo .')
        if args.build:
            exit(0)

    if args.run:
        run('docker run --rm -it -p 8000:80 --name letusgo letusgo')
        exit(0)
    if args.bash:
        run('docker run --rm -it -p 8000:80 --name letusgo letusgo /bin/bash')
        exit(0)

    run('docker push azelf/letusgo:base')
    run('git add -A')
    run('git add -f .master')
    run('git add -f .secrets')
    run(f'eb deploy --staged {args.env} &')
    run('sleep 10')
    run('git reset HEAD', stdout=subprocess.DEVNULL)
