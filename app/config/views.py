from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView

__all__ = (
    'IndexView',
    'HealthCheckView',
)


class IndexView(TemplateView):
    template_name = 'index.jinja2'


class HealthCheckView(View):
    def get(self, request):
        return HttpResponse('ok')
