from django.urls import path
from django_aid.drf.drf_yasg import schema

from . import apis

app_name = "sponsors"
urlpatterns = [
    path(
        "tiers/",
        schema(
            apis.SponsorTierListAPIView,
            [("get", {"operation_description": "스폰서 등급 목록(등급별 스폰서 목록 포함)"},)],
        ).as_view(),
    ),
]
