from .production_master import *

# Secrets
AWS_SECRETS_MANAGER_SECRET_SECTION = "letusgo:ci"
AWS_STORAGE_BUCKET_NAME = SECRETS["AWS_STORAGE_BUCKET_NAME"]
ALLOWED_HOSTS = SECRETS["ALLOWED_HOSTS"]
SENTRY_DSN = SECRETS["SENTRY_DSN"]

# Email
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(ROOT_DIR, ".email")

# Sentry
sentry_sdk.init(
    dsn=SENTRY_DSN, integrations=[DjangoIntegration()], send_default_pii=True,
)
