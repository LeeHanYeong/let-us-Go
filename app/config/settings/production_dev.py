from .production_master import *
from .dev import *

LOCAL = False
DEBUG = True

# Secrets
AWS_SECRETS_MANAGER_SECRET_SECTION = "letusgo:production_dev"
AWS_STORAGE_BUCKET_NAME = SECRETS["AWS_STORAGE_BUCKET_NAME"]

ALLOWED_HOSTS = [
    "api-dev.letusgo.app",
]
DATABASES = SECRETS["DATABASES"]
API_KEY_FRONT_DEPLOY = SECRETS["API_KEY_FRONT_DEPLOY"]
SENTRY_DSN = SECRETS["SENTRY_DSN"]

# dbbackup
DBBACKUP_STORAGE = "config.storages.MediaStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": "db/"}

CORS_ORIGIN_ALLOW_ALL = True

# WSGI
WSGI_APPLICATION = "config.wsgi.production_dev.application"

# Sentry
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration()],
    environment=ENV,
    send_default_pii=True,
)
