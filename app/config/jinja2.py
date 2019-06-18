from django.contrib import messages
from django.templatetags.static import static
from django.urls import reverse
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
    })
    return env
