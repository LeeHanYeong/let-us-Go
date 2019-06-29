from .base import *

import_secrets()

DEBUG = True
ALLOWED_HOSTS += [
    'localhost',
    '127.0.0.1',
]

# Static
MEDIA_LOCATION = 'media_dev'
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'

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
