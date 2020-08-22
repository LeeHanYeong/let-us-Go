import datetime
from numbers import Integral

from django.conf import settings
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django.templatetags.static import static
from django.urls import reverse
from django.utils import dateformat
from django.utils.timezone import (
    template_localtime,
    localtime as timezone_localtime,
    localdate as timezone_localdate,
)
from jinja2 import Environment
from sentry_sdk import capture_message, capture_exception


def query(request=None, only=False, **kwargs):
    if request is None or only:
        query_params = kwargs
    else:
        query_params = {k: v for k, v in request.GET.items() if v}
        query_params.update(kwargs)
        query_params = {k: v for k, v in query_params.items() if v}

    if query_params:
        return "?" + "&".join([f"{k}={v}" for k, v in query_params.items()])
    return ""


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


def price(value):
    if isinstance(value, Integral) and value != 0:
        return f"{value:,}원"
    return "없음"


def localtime(value, time_format=settings.TIME_FORMAT):
    try:
        return dateformat.time_format(value, time_format)
    except Exception as e:
        capture_exception(e)
        return value


def localdate(value, date_format=settings.DATE_FORMAT):
    try:
        return dateformat.format(timezone_localdate(value), date_format)
    except Exception as e:
        capture_exception(e)
        return value


def localdatetime(value, datetime_format=settings.DATETIME_FORMAT):
    try:
        return dateformat.format(timezone_localtime(value), datetime_format)
    except Exception as e:
        capture_exception(e)
        return value


def environment(**options):
    extensions = options.get("extensions", [])
    options["extensions"] = extensions

    env = Environment(**options)
    env.globals.update(
        {
            "static": static,
            "url": reverse,
            "query": query,
            "get_messages": messages.get_messages,
            "localtime": localtime,
            "localdate": localdate,
            "localdatetime": localdatetime,
        }
    )
    env.filters.update(
        {"date": date, "time": time, "intcomma": intcomma, "price": price,}
    )
    return env
