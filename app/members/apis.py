from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from .models import User
from .permissions import IsUserSelf
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='User Create',
        operation_description='사용자 생성'
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
        operation_description='사용자 정보 수정'
    )
)
@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(
        operation_summary='User Delete',
        operation_description='사용자 삭제(탈퇴)'
    )
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