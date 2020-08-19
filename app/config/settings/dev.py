from .base import *

# Secrets
AWS_SECRETS_MANAGER_SECRET_SECTION = 'letusgo:dev'
DATABASES = SECRETS['DATABASES']
API_KEY_FRONT_DEPLOY = SECRETS['API_KEY_FRONT_DEPLOY']

DEBUG = True
ALLOWED_HOSTS += [
    'localhost',
    '127.0.0.1',
]

WSGI_APPLICATION = 'config.wsgi.dev.application'
INSTALLED_APPS += [
    'debug_toolbar',
    'sslserver',
]
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# django-debug-toolbar
INTERNAL_IPS = ['127.0.0.1']

# django-cors-headers
CORS_ORIGIN_ALLOW_ALL = True
