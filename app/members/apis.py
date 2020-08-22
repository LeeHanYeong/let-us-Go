from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django_aid.drf.viewsets import ModelViewSet
from djangorestframework_camel_case.util import camel_to_underscore
from drf_yasg.utils import swagger_auto_schema
from rest_auth.views import LoginView
from rest_framework import generics, status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .models import User, EmailVerification
from .permissions import IsUserSelf
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserAttributeAvailableSerializer,
    AuthTokenSerializer,
    EmailVerificationCreateSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.annotate_choices()
    serializer_classes = {
        "list": UserSerializer,
        "retrieve": UserSerializer,
        "create": UserCreateSerializer,
        "update": UserUpdateSerializer,
        "profile": UserSerializer,
        "available": UserAttributeAvailableSerializer,
    }

    @action(detail=False, methods=["get"])
    def profile(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(detail=False, methods=["post"])
    def available(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            attribute_name = camel_to_underscore(
                serializer.validated_data["attribute_name"]
            )
            value = serializer.validated_data["value"]
            filter_kwargs = {
                attribute_name: value,
            }
            exists = User.objects.filter(is_deleted=False, **filter_kwargs).exists()
            data = {
                "exists": exists,
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        if self.action == "profile":
            return self.request.user
        return super().get_object()

    def get_permissions(self):
        if self.action in ("retrieve", "update", "delete"):
            return [IsUserSelf]
        elif self.action == "profile":
            return [permissions.IsAuthenticated]
        return []


class AuthTokenAPIView(LoginView):
    def get_response_serializer(self):
        return AuthTokenSerializer


class EmailVerificationCreateAPIView(generics.CreateAPIView):
    queryset = EmailVerification.objects.all()
    serializer_class = EmailVerificationCreateSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        subject = "let us: Go! 회원가입 이메일 인증 안내메일입니다"
        result = send_mail(
            subject=subject,
            message=subject,
            html_message=render_to_string(
                template_name="members/email-validation.jinja2",
                context={
                    "subject": subject,
                    "site": get_current_site(self.request),
                    "code": instance.code,
                },
                request=self.request,
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
        )
        instance.status_send = (
            EmailVerification.SUCCEED if result == 1 else EmailVerification.FAILED
        )
        instance.save()
        if result == 0:
            raise APIException("인증 이메일 발송에 실패했습니다")
