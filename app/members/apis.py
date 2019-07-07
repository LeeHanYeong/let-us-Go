from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from djangorestframework_camel_case.util import camel_to_underscore
from drf_yasg.openapi import Response as APIResponse
from drf_yasg.utils import swagger_auto_schema
from rest_auth.views import LoginView
from rest_framework import generics, status, permissions
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from utils.drf import errors
from utils.drf.doc import ResponseErrors
from .models import User, EmailVerification
from .permissions import IsUserSelf
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserAttributeAvailableSerializer,
    AuthTokenSerializer, EmailVerificationCreateSerializer)


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='User Create',
        operation_description='사용자 생성',
        responses={
            status.HTTP_200_OK: UserSerializer(),
            status.HTTP_400_BAD_REQUEST: APIResponse(
                description='실패',
                examples={
                    **ResponseErrors(
                        '이메일 인증 관련',
                        errors.EMAIL_SEND_FAILED,
                        errors.EMAIL_VERIFICATION_INCOMPLETED,
                        errors.EMAIL_VERIFICATION_NOT_EXISTS,
                    ),
                }
            ),
        }
    )
)
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='User Retrieve',
        operation_description='사용자 정보'
    )
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        operation_summary='User Update',
        operation_description='사용자 정보 수정',
        responses={
            status.HTTP_200_OK: UserSerializer(),
        },
    ),
)
@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(
        operation_summary='User Delete',
        operation_description='사용자 삭제(탈퇴)',
    ),
)
class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsUserSelf,)

    def get_serializer_class(self):
        if self.request.method in ('PATCH', 'PUT'):
            return UserUpdateSerializer
        return UserSerializer

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        super().put(request, *args, **kwargs)


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='User Profile',
        operation_description='사용자 프로필 (인증필요, 인증되어있는 경우 자신의 정보)'
    )
)
class UserProfileAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='AuthToken',
        operation_description='인증정보를 사용해 사용자의 Token(key)과 User정보를 획득',
        responses={
            status.HTTP_200_OK: AuthTokenSerializer(),
        }
    ),
)
class AuthTokenAPIView(LoginView):
    def get_response_serializer(self):
        return AuthTokenSerializer


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='EmailVerification',
        operation_description='이메일 인증<br>요청시 사용자에게 인증메일을 발송하며, 인증이 완료된 이메일로만 회원가입(UserCreate)이 성공합니다',
    ),
)
class EmailVerificationCreateAPIView(generics.CreateAPIView):
    queryset = EmailVerification.objects.all()
    serializer_class = EmailVerificationCreateSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        subject = 'let us: Go! 회원가입 이메일 인증 안내메일입니다'
        result = send_mail(
            subject=subject,
            message=subject,
            html_message=render_to_string(
                template_name='members/email-validation.jinja2',
                context={
                    'subject': subject,
                    'site': get_current_site(self.request),
                    'code': instance.code,
                },
                request=self.request,
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
        )
        instance.status_send = EmailVerification.SUCCEED if result == 1 else EmailVerification.FAILED
        instance.save()
        if result == 0:
            raise APIException('인증 이메일 발송에 실패했습니다')


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='UserAttribute Available Check',
        operation_description='사용자 생성 시 속성값 사용가능(중복)여부 체크',
        responses={
            status.HTTP_200_OK: APIResponse(
                description='',
                examples={
                    'application/json': {
                        'exists': True,
                    }}
            ),
        }
    ),
)
class UserAttributeAvailableAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserAttributeAvailableSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            attribute_name = camel_to_underscore(serializer.validated_data['attribute_name'])
            value = serializer.validated_data['value']
            filter_kwargs = {
                attribute_name: value,
            }
            exists = User.objects.filter(is_deleted=False, **filter_kwargs).exists()
            data = {
                'exists': exists,
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
