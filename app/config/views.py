import os

from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView

__all__ = (
    "IndexView",
    "HealthCheckView",
)


class IndexView(TemplateView):
    template_name = "index.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings_module"] = os.environ.get("DJANGO_SETTINGS_MODULE")
        return context


class HealthCheckView(View):
    def get(self, request):
        return HttpResponse("ok")
