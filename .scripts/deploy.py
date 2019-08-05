#!/usr/bin/env python
import argparse
import json
import os
import shutil
import subprocess
from time import sleep

import boto3

parser = argparse.ArgumentParser()
parser.add_argument('--build', action='store_true')
parser.add_argument('--run', action='store_true')
parser.add_argument('--bash', action='store_true')
args = parser.parse_args()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')

MASTER_DIR = os.path.join(ROOT_DIR, '.master')
MASTER_TAR_PATH = os.path.join(ROOT_DIR, '.master.tar')
MASTER_SECRETS_DIR = os.path.join(ROOT_DIR, '.master', '.secrets')
SECRETS = json.load(open(os.path.join(SECRETS_DIR, 'base.json')))

ACCESS_KEY = SECRETS['AWS_EB_ACCESS_KEY_ID']
SECRET_KEY = SECRETS['AWS_EB_SECRET_ACCESS_KEY']
os.environ['AWS_ACCESS_KEY_ID'] = ACCESS_KEY
os.environ['AWS_SECRET_ACCESS_KEY'] = SECRET_KEY
ENV = dict(os.environ, AWS_ACCESS_KEY_ID=ACCESS_KEY, AWS_SECRET_ACCESS_KEY=SECRET_KEY)
ENV['PYTHONPATH'] = ENV.get('PYENV_VIRTUAL_ENV') or ENV.get('VIRTUAL_ENV')

# Docker Images
IMAGE_BASE = 'azelf/letusgo:base'
IMAGE_PRODUCTION_LOCAL = 'letusgo'
IMAGE_PRODUCTION_ECR = '347809506342.dkr.ecr.ap-northeast-2.amazonaws.com/letusgo:app'

# EB Variables
ENV_NAME_BLUE = 'letusgo-blue'
ENV_NAME_GREEN = 'letusgo-green'
CNAME_PREFIX = 'letusgo.'

# Docker commands
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


def build():
    os.chdir(ROOT_DIR)
    os.makedirs(os.path.join(ROOT_DIR, '.temp'), exist_ok=True)

    # Clone Front Project
    FRONT_DIR = os.path.join(ROOT_DIR, '.front')
    if os.path.exists(FRONT_DIR):
        os.chdir(FRONT_DIR)
        run('git pull')
    else:
        run('git clone https://github.com/Yuni-Q/proj2.git .front')
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

    # Build local image
    run(f'docker build -t {IMAGE_PRODUCTION_LOCAL} -f Dockerfile .')


if __name__ == '__main__':
    os.chdir(ROOT_DIR)
    # 로컬 이미지 빌드
    build()

    # build/run/bash옵션 처리
    if args.build:
        exit(0)

    if args.run:
        run(f'{RUN_CMD}')
        exit(0)

    if args.bash:
        run(f'{RUN_CMD} /bin/bash')
        exit(0)

    # 위 3경우 외에는 deploy이므로, 이미지 push후 진행
    run(f'docker push {IMAGE_BASE}')

    # AWS Clients
    client = boto3.client('elasticbeanstalk')
    elb_client = boto3.client('elbv2')
    ec2_client = boto3.client('ec2')

    # 실행중인 Environment가져오기
    environments = [
        environment for environment in client.describe_environments()['Environments']
        if environment['Status'] != 'Terminated'
    ]
    if len(environments) != 1:
        raise Exception(f'실행중인 환경이 1개가 아닙니다 (총 {len(environments)}개)')
    environment = environments[0]

    # 실행중인 Environment의 Name, 새로 생성해서 Swap할 Environment의 Name
    environment_name = environment['EnvironmentName']
    swap_environment_name = ENV_NAME_GREEN if environment_name == ENV_NAME_BLUE else ENV_NAME_BLUE
    print(f'실행중인 Environment: {environment_name}')
    print(f'새로 생성할 Environment: {swap_environment_name}')

    # eb create
    run(f'eb create {swap_environment_name} --cname letusgo-swap --elb-type application --sample')

    # staged영역 포함한 eb deploy실행
    run('git add -A')
    run('git add -f .master')
    run('git add -f .secrets')
    run(f'eb deploy --staged --timeout 20 {swap_environment_name}')
    run('git reset HEAD', stdout=subprocess.DEVNULL)

    # 새로 생성한 Environment의 LoadBalancer
    swap_load_balancer = client.describe_environment_resources(
        EnvironmentName=swap_environment_name
    )['EnvironmentResources']['LoadBalancers'][0]

    # 새로 생성한 LoadBalancer의 TargetGroup
    swap_target_group = elb_client.describe_target_groups(
        LoadBalancerArn=swap_load_balancer['Name'],
    )['TargetGroups'][0]['TargetGroupArn']

    # 새로 생성한 LoadBalancer의 SecurityGroup
    swap_security_group_id = elb_client.describe_load_balancers(
        LoadBalancerArns=[swap_load_balancer['Name']]
    )['LoadBalancers'][0]['SecurityGroups'][0]

    # 새 LoadBalancer에 HTTPS Listener추가 및 ACM추가
    elb_client.create_listener(
        LoadBalancerArn=swap_load_balancer['Name'],
        Protocol='HTTPS',
        Port=443,
        Certificates=[
            {
                'CertificateArn': SECRETS['AWS_ACM_ARN'],
            },
        ],
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': swap_target_group,
            }
        ]
    )

    # 새 LoadBalancer의 securityGroup에 443Port Inbound추가
    ec2_client.authorize_security_group_ingress(
        GroupId=swap_security_group_id,
        IpPermissions=[
            {
                'FromPort': 443,
                'IpProtocol': 'tcp',
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}],
                'Ipv6Ranges': [{'CidrIpv6': '::/0'}],
                'ToPort': 443,
            }
        ]
    )

    # CName Swap
    client.swap_environment_cnames(
        SourceEnvironmentName=environment_name,
        DestinationEnvironmentName=swap_environment_name,
    )

    # 새 Environment의 CNAME이 CNAME_PREFIX로 시작할때까지 기다림
    while True:
        cname = client.describe_environments(
            EnvironmentNames=[swap_environment_name],
        )['Environments'][0]['CNAME']
        sleep(5)
        if CNAME_PREFIX in cname:
            break

    # 기존 Environment terminate
    client.terminate_environment(
        EnvironmentName=environment_name,
    )
    print('완료')
