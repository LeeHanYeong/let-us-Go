from .production_master import *
from .dev import *

DEBUG = True

# Secrets
AWS_SECRETS_MANAGER_SECRET_SECTION = "letusgo:production_dev"
AWS_STORAGE_BUCKET_NAME = SECRETS["AWS_STORAGE_BUCKET_NAME"]
ALLOWED_HOSTS += SECRETS["ALLOWED_HOSTS"]
DATABASES = SECRETS["DATABASES"]
API_KEY_FRONT_DEPLOY = SECRETS["API_KEY_FRONT_DEPLOY"]
SENTRY_DSN = SECRETS["SENTRY_DSN"]

CORS_ORIGIN_ALLOW_ALL = True

# WSGI
WSGI_APPLICATION = "config.wsgi.production_dev.application"

if private_ip:
    # Sentry
    sentry_sdk.init(
        dsn=SENTRY_DSN, integrations=[DjangoIntegration()], send_default_pii=True,
    )
else:
    ALLOWED_HOSTS += [
        "api.dev.localhost",
    ]
