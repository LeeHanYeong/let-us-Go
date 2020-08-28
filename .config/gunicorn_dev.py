daemon = False
chdir = "/srv/app"
bind = "0.0.0.0:8001"
worker_class = "gevent"
workers = 1
threads = 1
timeout = 60
accesslog = "/var/log/gunicorn/dev_access.log"
errorlog = "/var/log/gunicorn/dev_error.log"
capture_output = False
raw_env = [
    "DJANGO_SETTINGS_MODULE=config.settings.production_dev",
]
