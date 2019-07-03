daemon = False
chdir = '/srv/master/app'
bind = 'unix:/tmp/app.sock'
worker_class = 'gevent'
workers = 4
timeout = 60
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
capture_output = True
raw_env = [
    'DJANGO_SETTINGS_MODULE=config.settings.production_master',
]
