from .base import *

DEBUG = True
ALLOWED_HOSTS += [
    'localhost',
    '.localhost',
    '127.0.0.1',
]

# Secrets
AWS_SECRETS_MANAGER_SECRET_SECTION = 'letusgo:dev'
API_KEY_FRONT_DEPLOY = SECRETS['API_KEY_FRONT_DEPLOY']
DATABASES = SECRETS['DATABASES']

# dev settings
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
