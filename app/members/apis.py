from django_aid.drf.viewsets import ModelViewSet, ViewSetMixin
from djangorestframework_camel_case.util import camel_to_underscore
from rest_framework import permissions, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import User, EmailVerification
from .permissions import IsUserSelf
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserAttributeAvailableSerializer,
    EmailVerificationCreateSerializer,
    EmailVerificationCheckSerializer,
    GetEmailAuthTokenSerializer,
    AuthTokenSerializer,
    UserPasswordResetRequestSerializer,
    UserPasswordResetSerializer,
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
        "password_reset_request": UserPasswordResetRequestSerializer,
        "password_reset": UserPasswordResetSerializer,
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

    @action(detail=False, methods=["post"])
    def password_reset_request(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        ev = serializer.save()
        ev.send()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"])
    def password_reset(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.set_password(serializer.validated_data["password"])
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


class AuthTokenAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GetEmailAuthTokenSerializer(
            data=request.data, context={"reuqest": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        token_serializer = AuthTokenSerializer(token)
        return Response(token_serializer.data)


class EmailVerificationViewSet(ViewSetMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = EmailVerification.objects.all()
    serializer_classes = {
        "create": EmailVerificationCreateSerializer,
        "check": EmailVerificationCheckSerializer,
    }

    def perform_create(self, serializer):
        ev = serializer.save()
        ev.send()

    @action(detail=False, methods=["post"])
    def check(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
