#!/usr/bin/env python
import argparse
import json
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('env', type=str)
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
    run(f'eb create {args.env} --cname {args.env} --elb-type application --sample')
