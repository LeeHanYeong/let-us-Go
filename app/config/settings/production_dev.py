from .production_master import *

from aws_secrets import SECRETS

# Secrets
AWS_SECRETS_MANAGER_SECRETS_SECTION = 'letusgo:production_dev'
ALLOWED_HOSTS = SECRETS['ALLOWED_HOSTS']
DATABASES = SECRETS['DATABASES']
AWS_STORAGE_BUCKET_NAME = SECRETS['AWS_STORAGE_BUCKET_NAME']
API_KEY_FRONT_DEPLOY = SECRETS['API_KEY_FRONT_DEPLOY']

DEBUG = True

# WSGI
WSGI_APPLICATION = 'config.wsgi.production_dev.application'

if not private_ip:
    DEBUG = True
    ALLOWED_HOSTS += [
        'localhost',
        'dev.api.localhost',
    ]
