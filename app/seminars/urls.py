from django.urls import path, include
from django_aid.drf.drf_yasg import schema
from drf_yasg.openapi import Parameter, IN_PATH
from rest_framework.routers import SimpleRouter

from . import apis

app_name = "seminars"

router = SimpleRouter()
router.register(
    r"",
    schema(
        apis.SeminarViewSet,
        (
            ("list", {"operation_description": "세미나 목록"}),
            ("retrieve", {"operation_description": "세미나 상세"}),
        ),
    ),
)
router.register(
    r"tracks",
    schema(
        apis.TrackViewSet,
        (
            ("list", {"operation_description": "트랙 목록",}),
            ("retrieve", {"operation_description": "트랙 상세",}),
        ),
    ),
)
router.register(
    r"sessions",
    schema(
        apis.SessionViewSet,
        (
            ("list", {"operation_description": "세션 목록",}),
            ("retrieve", {"operation_description": "세션 상세",}),
            (
                "search",
                {
                    "operation_description": "세션 검색",
                    "manual_parameters": [Parameter("keyword", IN_PATH, type="string")],
                },
            ),
        ),
    ),
)
router.register(
    r"speakers",
    schema(apis.SpeakerViewSet, (("list", {"operation_description": "발표자 목록",}),),),
)

urlpatterns = [
    path("", include(router.urls)),
]
