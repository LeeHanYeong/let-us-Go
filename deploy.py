#!/usr/bin/env python
import argparse
import json
import os
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('env', type=str)
parser.add_argument('--build', action='store_true')
parser.add_argument('--run', action='store_true')
parser.add_argument('--bash', action='store_true')
args = parser.parse_args()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')

MASTER_DIR = os.path.join(ROOT_DIR, '.master')
MASTER_TAR_PATH = os.path.join(ROOT_DIR, '.master.tar')
MASTER_SECRETS_DIR = os.path.join(ROOT_DIR, '.master', '.secrets')
SECRETS = json.load(open(os.path.join(SECRETS_DIR, 'base.json')))

ACCESS_KEY = SECRETS['AWS_EB_ACCESS_KEY_ID']
SECRET_KEY = SECRETS['AWS_EB_SECRET_ACCESS_KEY']
ENV = dict(os.environ, AWS_ACCESS_KEY_ID=ACCESS_KEY, AWS_SECRET_ACCESS_KEY=SECRET_KEY)
ENV['PYTHONPATH'] = ENV.get('PYENV_VIRTUAL_ENV') or ENV.get('VIRTUAL_ENV')

IMAGE_BASE = 'azelf/letusgo:base'
IMAGE_PRODUCTION_LOCAL = 'letusgo'
IMAGE_PRODUCTION_ECR = '347809506342.dkr.ecr.ap-northeast-2.amazonaws.com/letusgo:app'

RUN_OPTIONS = (
    '-p 8000:80',
    '--name letusgo',
    '--memory=1024m',
    '--memory-swap=1536m',
    '--cpus=1',
    'letusgo',
)
RUN_CMD = 'docker run --rm -it {options}'.format(
    options=' '.join([option for option in RUN_OPTIONS])
)


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
    run(f'docker build -t {IMAGE_BASE} -f .dockerfile/Dockerfile.base .')

    # master코드 분리
    run(f'rm -rf {MASTER_DIR}')
    os.makedirs(MASTER_DIR, exist_ok=True)
    run(f'git archive --format=tar.gz master -o {MASTER_TAR_PATH}')
    run(f'tar -xzf {MASTER_TAR_PATH} -C {MASTER_DIR}')
    os.remove(MASTER_TAR_PATH)
    shutil.rmtree(MASTER_SECRETS_DIR, ignore_errors=True)
    shutil.copytree(SECRETS_DIR, MASTER_SECRETS_DIR)

    # migrate
    run('DJANGO_SETTINGS_MODULE=config.settings.production_dev python app/manage.py migrate --noinput')
    os.chdir(os.path.join(ROOT_DIR, '.master'))
    run('DJANGO_SETTINGS_MODULE=config.settings.production_master python app/manage.py migrate --noinput')
    os.chdir(os.path.join(ROOT_DIR))

    if args.build or args.run or args.bash:
        run(f'docker build -t {IMAGE_PRODUCTION_LOCAL} -f Dockerfile.production .')
        if args.build:
            exit(0)

    if args.run:
        run(f'{RUN_CMD}')
        exit(0)
    if args.bash:
        run(f'{RUN_CMD} /bin/bash')
        exit(0)

    # Push BaseImage
    run(f'docker push {IMAGE_BASE}')

    # Push ECR
    # run(f'docker build -t {IMAGE_PRODUCTION_LOCAL} -f Dockerfile.production .')
    # run(f'docker tag {IMAGE_PRODUCTION_LOCAL} {IMAGE_PRODUCTION_ECR}')
    # run(f'$(aws ecr get-login --no-include-email --region ap-northeast-2) && '
    #     f'docker push {IMAGE_PRODUCTION_ECR}')

    run('git add -A')
    run('git add -f .master')
    run('git add -f .secrets')
    run(f'eb deploy --staged {args.env} &')
    run('sleep 10')
    run('git reset HEAD', stdout=subprocess.DEVNULL)
