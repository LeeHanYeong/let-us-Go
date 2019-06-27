from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from .models import Attend
from .serializers import (
    AttendSerializer,
    AttendCreateSerializer,
    AttendDetailSerializer,
    AttendUpdateSerializer,
)

User = get_user_model()


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Attend List',
        operation_description='지원서 목록'
    )
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_summary='Attend Create',
        operation_description='지원서 작성'
    )
)
class AttendListCreateAPIView(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Attend.objects.select_related('seminar', 'user')
        if self.request.user.is_authenticated:
            return queryset.filter(user=self.request.user)
        return queryset.none()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AttendCreateSerializer
        return AttendSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Attend Retrieve',
        operation_description='지원서 정보'
    )
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        operation_summary='Attend Update',
        operation_description='지원서 정보 수정'
    )
)
class AttendRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Attend.objects.select_related('seminar', 'user')

    def get_serializer_class(self):
        if self.request.method in ('PATCH', 'PUT'):
            return AttendUpdateSerializer
        return AttendDetailSerializer

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
