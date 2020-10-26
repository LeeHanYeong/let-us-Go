from django.urls import path, include
from django_aid.drf.drf_yasg import schema
from drf_yasg.openapi import Response as APIResponse
from rest_framework import status
from rest_framework.routers import SimpleRouter

from . import apis
from .serializers import (
    UserSerializer,
    AuthTokenSerializer,
    GetEmailAuthTokenSerializer,
    GetSocialAuthTokenSerializer,
)

members_router = SimpleRouter()
members_router.register(
    r"users",
    schema(
        apis.UserViewSet,
        (
            ("list", {"operation_description": "사용자 목록"}),
            (
                "create",
                {
                    "operation_description": """
사용자 생성

> 가입 방식에 따라 필수 필드가 다름
- 이메일 가입 시: `password1`, `password2`
- 소셜 가입 시: `uid`
""",
                    "responses": {
                        status.HTTP_200_OK: UserSerializer(),
                        status.HTTP_400_BAD_REQUEST: APIResponse(
                            description="실패", examples={}
                        ),
                    },
                },
            ),
            ("retrieve", {"operation_description": "사용자 상세"}),
            (
                "update",
                {
                    "operation_description": "사용자 수정",
                    "responses": {status.HTTP_200_OK: UserSerializer()},
                },
            ),
            ("destroy", {"operation_description": "사용자 삭제(탈퇴)"}),
            (
                "profile",
                {
                    "operation_description": "사용자 프로필 (인증된 경우)",
                    "responses": {status.HTTP_200_OK: UserSerializer()},
                },
            ),
            (
                "available",
                {
                    "operation_summary": "UserAttribute Available Check",
                    "operation_description": "사용자 생성 시 속성값 사용가능(중복)여부 체크",
                    "responses": {
                        status.HTTP_200_OK: APIResponse(
                            description="",
                            examples={"application/json": {"exists": True}},
                        ),
                    },
                },
            ),
            (
                "password_reset_request",
                {
                    "operation_id": "members_z_password_reset_1",
                    "operation_summary": "Password Reset Email Request",
                    "operation_description": "비밀번호 변경 인증 이메일 요청",
                    "responses": {
                        status.HTTP_204_NO_CONTENT: APIResponse(
                            description="성공시 내용 없이 204 상태코드 응답"
                        ),
                    },
                },
            ),
            (
                "password_reset",
                {
                    "operation_id": "members_z_password_reset_2",
                    "operation_summary": "Password Reset",
                    "operation_description": "비밀번호 변경",
                    "responses": {
                        status.HTTP_200_OK: UserSerializer,
                    },
                },
            ),
        ),
    ),
)

members_patterns = ([path("", include(members_router.urls))], "members")

auth_router = SimpleRouter()
auth_router.register(
    r"email-verification",
    schema(
        apis.EmailVerificationViewSet,
        (
            (
                "create",
                {
                    "operation_summary": "EmailVerification Request",
                    "operation_description": "이메일 인증 요청",
                },
            ),
            (
                "check",
                {
                    "operation_summary": "EmailVerification Check",
                    "operation_description": "이메일 인증 확인",
                    "responses": {
                        status.HTTP_204_NO_CONTENT: APIResponse(
                            description="성공시 내용 없이 204 상태코드 응답"
                        ),
                    },
                },
            ),
        ),
    ),
)
auth_router.register(
    r"token",
    schema(
        apis.AuthTokenViewSet,
        [
            (
                "create",
                {
                    "operation_id": "auth_email_get_auth_token",
                    "operation_summary": "Get EmailAuthToken",
                    "operation_description": "인증정보를 사용해 사용자의 Token(key)과 User정보를 획득",
                    "request_body": GetEmailAuthTokenSerializer,
                    "responses": {
                        status.HTTP_200_OK: AuthTokenSerializer(),
                    },
                },
            ),
            (
                "social",
                {
                    "operation_id": "auth_social_get_auth_token",
                    "operation_summary": "Get SocialAuthToken",
                    "operation_description": "OAuth인증된 사용자 고유값을 사용해 사용자의 Token(key)과 User정보를 획득",
                    "request_body": GetSocialAuthTokenSerializer,
                    "responses": {
                        status.HTTP_200_OK: AuthTokenSerializer(),
                    },
                },
            ),
        ],
    ),
)
auth_patterns = ([path("", include(auth_router.urls))], "auth")
