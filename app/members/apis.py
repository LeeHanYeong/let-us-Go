from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_aid.drf.viewsets import ModelViewSet, ViewSetMixin
from djangorestframework_camel_case.util import camel_to_underscore
from rest_auth.views import LoginView
from rest_framework import permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from sentry_sdk import capture_exception

from utils.drf.exceptions import EmailSendFailed
from .models import User, EmailVerification
from .permissions import IsUserSelf
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserAttributeAvailableSerializer,
    AuthTokenSerializer,
    EmailVerificationCreateSerializer,
    EmailVerificationCheckSerializer,
)

__all__ = (
    "UserViewSet",
    "AuthTokenAPIView",
    "EmailVerificationViewSet",
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.annotate_choices()
    serializer_classes = {
        "list": UserSerializer,
        "create": UserCreateSerializer,
        "retrieve": UserSerializer,
        "update": UserUpdateSerializer,
        "profile": UserSerializer,
        "available": UserAttributeAvailableSerializer,
    }
    http_method_names = ["get", "post", "put", "patch", "head", "options", "trace"]

    @action(detail=False, methods=["get"])
    def profile(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(detail=False, methods=["post"])
    def available(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        attribute_name = camel_to_underscore(
            serializer.validated_data["attribute_name"]
        )
        value = serializer.validated_data["value"]
        filter_kwargs = {
            attribute_name: value,
        }
        exists = User.objects.filter(**filter_kwargs).exists()
        data = {
            "exists": exists,
        }
        return Response(data)

    def get_object(self):
        if self.action == "profile":
            return self.request.user
        return super().get_object()

    def get_permissions(self):
        if self.action in ("retrieve", "partial_update", "update"):
            return [IsUserSelf()]
        elif self.action in ("list", "profile"):
            return [permissions.IsAuthenticated()]
        return []


class AuthTokenAPIView(LoginView):
    def get_response_serializer(self):
        return AuthTokenSerializer


class EmailVerificationViewSet(ViewSetMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = EmailVerification.objects.all()
    serializer_classes = {
        "create": EmailVerificationCreateSerializer,
        "check": EmailVerificationCheckSerializer,
    }

    def perform_create(self, serializer):
        instance = serializer.save()
        subject = "let us: Go! 이메일 인증 코드"
        result = send_mail(
            subject=subject,
            message=instance.code,
            html_message=render_to_string(
                template_name="members/email-validation.jinja2",
                context={"subject": subject, "code": instance.code,},
                request=self.request,
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )
        # 해당 이메일로 마지막으로 인증요청한 항목 외에 삭제
        EmailVerification.objects.filter(email=instance.email).exclude(
            id=instance.id
        ).delete()
        if result == 1:
            instance.status_send = EmailVerification.SUCCEED
            instance.save()
        elif result == 0:
            instance.status_send = EmailVerification.FAILED
            instance.save()
            e = EmailSendFailed(f"인증 이메일 발송에 실패했습니다({instance.email})")
            capture_exception(e)
            raise e

    @action(detail=False, methods=["post"])
    def check(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
