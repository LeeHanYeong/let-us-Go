import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django.templatetags.static import static
from django.urls import reverse
from django.utils import dateformat
from django.utils.timezone import template_localtime
from jinja2 import Environment


def query(request=None, only=False, **kwargs):
    if request is None or only:
        query_params = kwargs
    else:
        query_params = {k: v for k, v in request.GET.items() if v}
        query_params.update(kwargs)
        query_params = {k: v for k, v in query_params.items() if v}

    if query_params:
        return '?' + '&'.join([f'{k}={v}' for k, v in query_params.items()])
    return ''


def date(value):
    if isinstance(value, datetime.datetime):
        return dateformat.format(value, settings.DATETIME_FORMAT)
    elif isinstance(value, datetime.date):
        return dateformat.format(value, settings.DATE_FORMAT)
    elif isinstance(value, datetime.time):
        return dateformat.format(value, settings.TIME_FORMAT)
    return value


def time(value):
    try:
        return dateformat.format(value, settings.TIME_FORMAT)
    except Exception:
        return value


def environment(**options):
    extensions = options.get('extensions', [])
    extensions.append('sass_processor.jinja2.ext.SassSrc')
    options['extensions'] = extensions

    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'query': query,
        'get_messages': messages.get_messages,
        'localtime': template_localtime,
    })
    env.filters.update({
        'localtime': template_localtime,
        'date': date,
        'time': time,
        'intcomma': intcomma,
    })
    return env
