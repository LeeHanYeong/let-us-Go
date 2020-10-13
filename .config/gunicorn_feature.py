daemon = False
chdir = "/srv/app"
bind = "0.0.0.0:8000"
worker_class = "gevent"
workers = 1
threads = 1
timeout = 60
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
capture_output = False
raw_env = [
    "DJANGO_SETTINGS_MODULE=config.settings.production_dev",
]
