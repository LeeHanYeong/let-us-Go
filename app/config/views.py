from django.views.generic import TemplateView

__all__ = (
    'IndexView',
)


class IndexView(TemplateView):
    template_name = 'index.jinja2'
