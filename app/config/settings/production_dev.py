from .production_master import *

secrets = import_secrets()

DEBUG = True

# WSGI
WSGI_APPLICATION = 'config.wsgi.production_dev.application'

if not private_ip:
    DEBUG = True
    ALLOWED_HOSTS += [
        'localhost',
        'dev.api.localhost',
    ]
