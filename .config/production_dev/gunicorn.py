daemon = False
chdir = '/srv/dev/app'
bind = 'unix:/tmp/app_dev.sock'
workers = 1
timeout = 60
accesslog = '/var/log/gunicorn/access_dev.log'
errorlog = '/var/log/gunicorn/error_dev.log'
capture_output = True
raw_env = [
    'DJANGO_SETTINGS_MODULE=config.settings.production_dev',
]
