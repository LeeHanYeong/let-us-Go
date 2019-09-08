"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from django.contrib import messages
from aws_secrets import SECRETS

from ..jinja2 import environment

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')
LOG_DIR = os.path.join(ROOT_DIR, '.log')
TEMP_DIR = os.path.join(ROOT_DIR, '.temp')
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

ALLOWED_HOSTS = []
SITE_ID = 1

# django-aws-secrets-manager
AWS_SECRETS_MANAGER_SECRETS_NAME = 'lhy'
# AWS_SECRETS_MANAGER_PROFILE = 'lhy-secrets-manager'
AWS_SECRETS_MANAGER_SECRETS_SECTION = 'letusgo:base'
AWS_SECRETS_MANAGER_REGION_NAME = 'ap-northeast-2'

SECRET_KEY = SECRETS['SECRET_KEY']

# django-storages
AWS_S3_ACCESS_KEY_ID = SECRETS['AWS_S3_ACCESS_KEY_ID']
AWS_S3_SECRET_ACCESS_KEY = SECRETS['AWS_S3_SECRET_ACCESS_KEY']
AWS_DEFAULT_ACL = SECRETS['AWS_DEFAULT_ACL']
AWS_BUCKET_ACL = SECRETS['AWS_BUCKET_ACL']
AWS_AUTO_CREATE_BUCKET = SECRETS['AWS_AUTO_CREATE_BUCKET']
AWS_S3_FILE_OVERWRITE = SECRETS['AWS_S3_FILE_OVERWRITE']

# Deploy
AWS_EB_ACCESS_KEY_ID = SECRETS['AWS_EB_ACCESS_KEY_ID']
AWS_EB_SECRET_ACCESS_KEY = SECRETS['AWS_EB_SECRET_ACCESS_KEY']
AWS_ACM_ARN = SECRETS['AWS_ACM_ARN']

# Email
EMAIL_HOST = SECRETS['EMAIL_HOST']
EMAIL_HOST_USER = SECRETS['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = SECRETS['EMAIL_HOST_PASSWORD']
EMAIL_PORT = SECRETS['EMAIL_PORT']
EMAIL_USE_TLS = SECRETS['EMAIL_USE_TLS']
DEFAULT_FROM_EMAIL = SECRETS['DEFAULT_FROM_EMAIL']

# Static
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
STATICFILES_DIRS = [STATIC_DIR]

MEDIA_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'

# easy-thumbnails
THUMBNAIL_DEFAULT_STORAGE = 'config.storages.MediaStorage'
THUMBNAIL_WIDGET_OPTIONS = {
    'size': (300, 300),
}
THUMBNAIL_ALIASES = {
    '': {
        'admin_list': {'size': (100, 100), 'crop': False},
    },
}

# Auth
AUTH_USER_MODEL = 'members.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'members.backends.SettingsBackend',
]
DEFAULT_USERS = {
    'dev@lhy.kr': {
        'password': 'pbkdf2_sha256$150000$89oDFBSARLc8$Jsv1BlODbmILIiENOq3/2cvQM4663zW+clxzm52Fo28=',
        'name': '이한영',
        'type': 'email',
        'phone_number': '010-4432-1234',
        'is_staff': True,
        'is_superuser': True,
    },
}

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'utils.drf.renderers.BrowsableAPIRendererWithoutForms',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'JSON_UNDERSCOREIZE': {
        'no_underscore_before_number': True,
    },
    'EXCEPTION_HANDLER': 'utils.drf.exceptions.custom_exception_handler',
}

# drf-yasg
TOKEN_DESCRIPTION = '''
### [DRF AuthToken](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
인증정보를 사용해 [AuthToken](#operation/auth_token_create) API에 요청, 결과로 돌아온 **key**를  
HTTP Request의 Header `Authorization`에 `Token <key>`값을 넣어 전송

```
Authorization: Token fs8943eu342cf79d8933jkd
``` 
'''
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'DRF AuthToken',
            'description': TOKEN_DESCRIPTION,
        }
    }
}

# AWS
AWS_AUTO_CREATE_BUCKET = True
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'ap-northeast-2'
AWS_DEFAULT_ACL = None

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Date/Time Format
DATE_FORMAT = 'Y년 m월 d일'
TIME_FORMAT = 'H시 i분'
DATETIME_FORMAT = f'{DATE_FORMAT} {TIME_FORMAT}'

# Messages tags
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# django-modeladmin-reorder
ADMIN_REORDER = (
    # 세미나
    {'app': 'seminars', 'label': '세미나', 'models': (
        {'model': 'seminars.Seminar', 'label': '세미나'},
        {'model': 'seminars.Track', 'label': '트랙'},
        {'model': 'seminars.Session', 'label': '세션'},
    )},
    {'app': 'seminars', 'label': '세미나 추가정보', 'models': (
        {'model': 'seminars.Speaker', 'label': '발표자'},
        {'model': 'seminars.SpeakerLinkType', 'label': '발표자 링크 유형'},
        {'model': 'seminars.SpeakerLink', 'label': '발표자 링크'},
        {'model': 'seminars.SessionVideo', 'label': '세션 영상'},
        {'model': 'seminars.SessionLink', 'label': '세션 링크'},
        {'model': 'seminars.SessionFile', 'label': '세션 첨부파일'},
    )},

    # 스폰서
    {'app': 'sponsors', 'label': '스폰서', 'models': (
        {'model': 'sponsors.SponsorTier', 'label': '스폰서 등급'},
        {'model': 'sponsors.Sponsor', 'label': '스폰서'},
    )},

    # 인증
    {'app': 'members', 'label': '인증 및 권한', 'models': (
        {'model': 'members.User', 'label': '사용자'},
        {'model': 'auth.Group', 'label': '그룹'},
        {'model': 'authtoken.Token', 'label': '인증토큰'},
        {'model': 'rest_framework_api_key.APIKey', 'label': 'APIKey'},
    )},
)

# django-phonenumber-field
PHONENUMBER_DEFAULT_REGION = 'KR'
PHONENUMBER_DB_FORMAT = 'NATIONAL'

# django-sass-processor, django-compressor
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]
COMPRESS_JINJA2_GET_ENVIRONMENT = environment

# ckeditor
CKEDITOR_UPLOAD_PATH = 'ckeditor/'
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Default',
        'toolbar_Default': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'Undo', 'Redo'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'], ['Source'],
        ],
    },
}

# Application definition
INSTALLED_APPS = [
    'attends.apps.AttendsConfig',
    'members.apps.MembersConfig',
    'seminars.apps.SeminarsConfig',
    'sponsors.apps.SponsorsConfig',
    'utils',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'adminsortable2',
    'django_cleanup.apps.CleanupConfig',
    'django_extensions',
    'django_filters',
    'drf_yasg',
    'corsheaders',
    'easy_thumbnails',
    'markdownx',
    'rest_auth',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_api_key',
    'oauth2_provider',
    'phonenumber_field',
    'sass_processor',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            os.path.join(TEMPLATES_DIR, 'jinja2'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'environment': 'config.jinja2.environment',
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATES_DIR,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(levelname)s] %(name)s (%(asctime)s)\n\t%(message)s'
        },
    },
    'handlers': {
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'formatter': 'default',
            'maxBytes': 1048576,
            'backupCount': 10,
        },
        'file_info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'filename': os.path.join(LOG_DIR, 'info.log'),
            'formatter': 'default',
            'maxBytes': 1048576,
            'backupCount': 10,
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
        },
    },
    'loggers': {
        'django': {
            'handlers': [
                'file_error',
                'file_info',
                'console',
            ],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
