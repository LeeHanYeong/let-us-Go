"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.renderers import ReDocRenderer as BaseReDocRenderer, OpenAPIRenderer
from drf_yasg.views import get_schema_view
from rest_framework import permissions

admin.site.site_title = 'let us:Go!'
admin.site.site_header = 'let us:Go! 관리자 페이지'

BaseSchemaView = get_schema_view(
    openapi.Info(
        title='let us: Go! API',
        default_version='v1',
        description='let us: Go! API Documentation',
        contact=openapi.Contact(email='dev@lhy.kr'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


class ReDocRenderer(BaseReDocRenderer):
    template = 'docs/redoc.html'


class RedocSchemaView(BaseSchemaView):
    renderer_classes = (ReDocRenderer, OpenAPIRenderer)


urlpatterns_apis_v1 = [
    path('seminars/', include('seminars.urls')),
]
urlpatterns = [
    re_path(r'^redoc/$', RedocSchemaView.as_cached_view(cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),

    path('api/v1/', include(urlpatterns_apis_v1)),
]
if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    except ModuleNotFoundError:
        pass
