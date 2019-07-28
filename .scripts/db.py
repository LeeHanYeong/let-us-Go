#!/usr/bin/env python
import argparse
import json
import os
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('command', type=str)
parser.add_argument('--production', action='store_true')
parser.add_argument('--dev', action='store_true')
args = parser.parse_args()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')

SECRETS_MASTER = json.load(open(os.path.join(SECRETS_DIR, 'production_master.json')))
DATABASE_HOST = SECRETS_MASTER['DATABASES']['default']['HOST']
DATABASE_NAME = SECRETS_MASTER['DATABASES']['default']['NAME']
DATABASE_USER = SECRETS_MASTER['DATABASES']['default']['USER']
DATABASE_PASSWORD = SECRETS_MASTER['DATABASES']['default']['PASSWORD']

SECRETS_DEV = json.load(open(os.path.join(SECRETS_DIR, 'production_dev.json')))
DATABASE_NAME_DEV = SECRETS_DEV['DATABASES']['default']['NAME']

ENV = dict(os.environ, PGPASSWORD=DATABASE_PASSWORD)


def run(cmd, **kwargs):
    subprocess.run(cmd, shell=True, env=ENV, **kwargs)


if __name__ == '__main__':
    os.chdir(ROOT_DIR)
    if args.production:
        TARGET_DB_NAME = DATABASE_NAME
        DUMP_DB_NAME = DATABASE_NAME_DEV
    elif args.dev:
        TARGET_DB_NAME = DATABASE_NAME_DEV
        DUMP_DB_NAME = DATABASE_NAME
    else:
        raise ValueError('--production또는 --dev옵션을 사용하십시오')

    if args.command == 'dump':
        run(f'pg_dump -h {DATABASE_HOST} {TARGET_DB_NAME} > db.dump')
    elif args.command == 'load':
        run(f'pg_dump -h {DATABASE_HOST} {DUMP_DB_NAME} > db.dump')
        run(f'dropdb -h {DATABASE_HOST} {TARGET_DB_NAME}')
        run(f'createdb -h {DATABASE_HOST} --owner=lhy --template=template0 --lc-collate="C" {TARGET_DB_NAME}')
        run(f'psql -h {DATABASE_HOST} {TARGET_DB_NAME} < db.dump')
        os.remove('db.dump')
