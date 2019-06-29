from django.utils.decorators import method_decorator
from drf_yasg.openapi import Response as APIResponse
from drf_yasg.utils import swagger_auto_schema
from rest_auth.views import LoginView
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .models import User
from .permissions import IsUserSelf
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserAttributeAvailableSerializer,
    AuthTokenSerializer)


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
            attribute_name = serializer.validated_data['attribute_name']
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


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='User Create',
        operation_description='사용자 생성',
        responses={
            status.HTTP_200_OK: UserSerializer(),
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
