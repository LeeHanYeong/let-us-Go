from .production_master import *

secrets = import_secrets()

DEBUG = True

# Static
MEDIA_LOCATION = 'media_dev'

if not private_ip:
    DEBUG = True
    ALLOWED_HOSTS.append('dev.api.localhost')
