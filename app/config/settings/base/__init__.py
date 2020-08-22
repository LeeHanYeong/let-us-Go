from django.contrib import messages

from .admin_reorder import *
from .auth import *
from .drf import *
from .drf_yasg import *
from .easy_thumbnails import *
from .paths import *
from .secrets import *
from .static import *

ALLOWED_HOSTS = []

# Date/Time Format
DATE_FORMAT = "Y년 m월 d일"
TIME_FORMAT = "H시 i분"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"
APPEND_SLASH = False

# Messages tags
MESSAGE_TAGS = {
    messages.DEBUG: "secondary",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}

# Application definition
INSTALLED_APPS = [
    "attends.apps.AttendsConfig",
    "members.apps.MembersConfig",
    "seminars.apps.SeminarsConfig",
    "sponsors.apps.SponsorsConfig",
    "utils",
    # Default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd-party
    "django_cleanup.apps.CleanupConfig",
    "django_extensions",
    "django_filters",
    "corsheaders",
    "easy_thumbnails",
    "phonenumber_field",
    # Admin
    "adminsortable2",
    "markdownx",
    # DRF
    "drf_yasg",
    "rest_auth",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_api_key",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "utils.django.middleware.AppendSlashMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "admin_reorder.middleware.ModelAdminReorder",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [os.path.join(TEMPLATES_DIR, "jinja2"),],
        "APP_DIRS": False,
        "OPTIONS": {"environment": "config.jinja2.environment",},
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR,],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGGING = {
    "version": 1,
    "formatters": {
        "default": {"format": "[%(levelname)s] %(name)s (%(asctime)s)\n\t%(message)s"},
    },
    "handlers": {
        "file_error": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "filename": os.path.join(LOG_DIR, "error.log"),
            "formatter": "default",
            "maxBytes": 1048576,
            "backupCount": 10,
        },
        "file_info": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "filename": os.path.join(LOG_DIR, "info.log"),
            "formatter": "default",
            "maxBytes": 1048576,
            "backupCount": 10,
        },
        "console": {"class": "logging.StreamHandler", "level": "INFO",},
    },
    "loggers": {
        "django": {
            "handlers": ["file_error", "file_info", "console",],
            "level": "INFO",
            "propagate": True,
        },
    },
}
