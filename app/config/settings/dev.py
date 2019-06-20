from .base import *

import_secrets()

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

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
