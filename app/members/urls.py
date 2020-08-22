from django.urls import path, include
from django_aid.drf.drf_yasg import schema
from drf_yasg.openapi import Response as APIResponse
from rest_framework import status
from rest_framework.routers import SimpleRouter

from . import apis
from .serializers import UserSerializer, AuthTokenSerializer

members_router = SimpleRouter()
members_router.register(
    r"users",
    schema(
        apis.UserViewSet,
        (
            ("list", {"operation_description": "사용자 목록",}),
            (
                "create",
                {
                    "operation_description": "사용자 생성",
                    "responses": {
                        status.HTTP_200_OK: UserSerializer(),
                        status.HTTP_400_BAD_REQUEST: APIResponse(
                            description="실패", examples={}
                        ),
                    },
                },
            ),
            ("retrieve", {"operation_description": "사용자 상세",}),
            (
                "update",
                {
                    "operation_description": "사용자 수정",
                    "responses": {status.HTTP_200_OK: UserSerializer()},
                },
            ),
            ("destroy", {"operation_description": "사용자 삭제(탈퇴)",}),
            ("profile", {"operation_description": "사용자 프로필 (인증된 경우)",}),
            (
                "available",
                {
                    "operation_summary": "UserAttribute Available Check",
                    "operation_description": "사용자 생성 시 속성값 사용가능(중복)여부 체크",
                    "responses": {
                        status.HTTP_200_OK: APIResponse(
                            description="",
                            examples={"application/json": {"exists": True,}},
                        ),
                    },
                },
            ),
        ),
    ),
)

members_patterns = (
    [path("", include(members_router.urls)),],
    "members",
)
auth_patterns = (
    [
        path(
            "token/",
            schema(
                apis.AuthTokenAPIView,
                [
                    (
                        "post",
                        {
                            "operation_id": "Get AuthToken",
                            "operation_description": "인증정보를 사용해 사용자의 Token(key)과 User정보를 획득",
                            "responses": {status.HTTP_200_OK: AuthTokenSerializer(),},
                        },
                    ),
                ],
            ).as_view(),
        ),
        path(
            "email-verification/",
            schema(
                apis.EmailVerificationCreateAPIView,
                [
                    (
                        "post",
                        {
                            "operation_summary": "EmailVerification",
                            "operation_description": "이메일 인증<br>요청시 사용자에게 인증메일을 발송하며, 인증이 완료된 이메일로만 회원가입(UserCreate)이 성공합니다",
                        },
                    )
                ],
            ).as_view(),
        ),
    ],
    "auth",
)
