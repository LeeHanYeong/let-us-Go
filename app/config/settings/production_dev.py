from .production_master import *

secrets = import_secrets()

DEBUG = True

# Static
MEDIA_LOCATION = 'media_dev'

if not private_ip:
    ALLOWED_HOSTS.append('dev.localhost')
print(ALLOWED_HOSTS)
