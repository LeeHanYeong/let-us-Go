import os

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .base import urlpatterns, urlpatterns_apis_v1

SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE")
if SETTINGS_MODULE in ("config.settings", "config.settings.dev"):
    try:
        import debug_toolbar

        urlpatterns += [
            path("__debug__/", include(debug_toolbar.urls)),
            *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
            *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        ]
        urlpatterns_apis_v1 += [
            # re_path(r"rest-auth/", include("rest_auth.urls")),
        ]
    except ModuleNotFoundError:
        pass
