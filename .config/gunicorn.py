daemon = False
chdir = '/srv/project/app'
bind = 'unix:/tmp/app.sock'
workers = 5
threads = 2
timeout = 60
access_logfile = '/var/log/gunicorn-access.log'
error_logfile = '/var/log/gunicorn-error.log'
