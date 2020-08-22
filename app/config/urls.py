import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from members import views as views_members
from members.urls import members_patterns, auth_patterns
from . import views, apis
from .doc import RedocSchemaView

admin.site.site_title = "let us:Go!"
admin.site.site_header = "let us:Go! 관리자 페이지"
admin.site.enable_nav_sidebar = False

urlpatterns_apis_utils = [
    path("front-deploy/", apis.FrontDeployAPIView.as_view(), name="front-deploy"),
]
urlpatterns_apis_v1 = [
    path("attends/", include("attends.urls")),
    path("auth/", include(auth_patterns)),
    path("members/", include(members_patterns)),
    path("seminars/", include("seminars.urls")),
    path("sponsors/", include("sponsors.urls")),
    path("utils/", include(urlpatterns_apis_utils)),
]
urlpatterns = [
    re_path(
        r"^doc/$", RedocSchemaView.as_cached_view(cache_timeout=0), name="schema-redoc"
    ),
    path("admin/", admin.site.urls),
    path("markdownx/", include("markdownx.urls")),
    path("health/", views.HealthCheckView.as_view(), name="health-check"),
    path("", views.IndexView.as_view(), name="index"),
    path(
        "email-validation/<str:code>/",
        views_members.EmailValidationView.as_view(),
        name="email-validation",
    ),
    path("v1/", include(urlpatterns_apis_v1)),
]
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
