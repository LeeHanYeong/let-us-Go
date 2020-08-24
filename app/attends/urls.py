from django.urls import path, include
from django_aid.drf.drf_yasg import schema
from rest_framework.routers import SimpleRouter

from . import apis

router = SimpleRouter()
router.register(
    r"",
    schema(
        apis.AttendModelViewSet,
        (
            ("list", {"operation_description": "지원서 목록"}),
            ("create", {"operation_description": "지원서 작성"}),
            ("retrieve", {"operation_description": "지원서 상세"}),
            ("update", {"operation_description": "지원서 수정"}),
            ("destroy", {"operation_description": "지원서 삭제"}),
        ),
    ),
)

urlpatterns = [
    path("", include(router.urls)),
]
