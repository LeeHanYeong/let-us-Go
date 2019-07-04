import platform
import sys

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

secrets = import_secrets()

DEBUG = False or (
        len(sys.argv) > 1
        and sys.argv[1] == 'runserver'
        and platform.system() != 'Linux'
) or os.environ.get('DEBUG') == 'True'

# WSGI
WSGI_APPLICATION = 'config.wsgi.production.application'

# Static
MEDIA_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'

# django-cors-headers
CORS_ORIGIN_ALLOW_ALL = True

# Sentry
sentry_sdk.init(
    dsn=secrets['SENTRY_DSN'],
    integrations=[DjangoIntegration()]
)

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


def is_ec2_linux():
    """
    Detect if we are running on an EC2 Linux Instance
    See http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/identify_ec2_instances.html
    """
    if os.path.isfile("/sys/hypervisor/uuid"):
        with open("/sys/hypervisor/uuid") as f:
            uuid = f.read()
            return uuid.startswith("ec2")
    return False


def get_linux_ec2_private_ip():
    """Get the private IP Address of the machine if running on an EC2 linux server"""
    from urllib.request import urlopen
    if not is_ec2_linux():
        return None
    try:
        response = urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
        ec2_ip = response.read().decode('utf-8')
        response = urlopen('http://169.254.169.254/latest/meta-data/local-hostname')
        ec2_hostname = response.read().decode('utf-8')
        return ec2_ip
    except Exception as e:
        print(e)
        return None


private_ip = get_linux_ec2_private_ip()
if private_ip:
    ALLOWED_HOSTS.append(private_ip)

    # SSL
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = False
    CSRF_COOKIE_SECURE = True
else:
    DEBUG = True
    ALLOWED_HOSTS.append('api.localhost')
