from django.contrib import admin
from django.urls import path, include, re_path

from members.urls import members_patterns, auth_patterns
from .. import views
from ..doc import RedocSchemaView

admin.site.site_title = "let us:Go!"
admin.site.site_header = "let us:Go! 관리자 페이지"
admin.site.enable_nav_sidebar = False

urlpatterns_apis_v1 = [
    path("attends/", include("attends.urls")),
    path("auth/", include(auth_patterns)),
    path("members/", include(members_patterns)),
    path("seminars/", include("seminars.urls")),
    path("sponsors/", include("sponsors.urls")),
]
urlpatterns = [
    re_path(
        r"^doc/$", RedocSchemaView.as_cached_view(cache_timeout=0), name="schema-redoc"
    ),
    path("admin/", admin.site.urls),
    path("markdownx/", include("markdownx.urls")),
    path("health/", views.HealthCheckView.as_view(), name="health-check"),
    path("", views.IndexView.as_view(), name="index"),
    path("v1/", include(urlpatterns_apis_v1)),
]