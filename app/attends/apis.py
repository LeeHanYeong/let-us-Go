from django.contrib.auth import get_user_model
from django_aid.drf.viewsets import ModelViewSet
from rest_framework import permissions

from .models import Attend
from .serializers import (
    AttendSerializer,
    AttendCreateSerializer,
    AttendDetailSerializer,
    AttendUpdateSerializer,
)

User = get_user_model()

__all__ = ("AttendModelViewSet",)


class AttendModelViewSet(ModelViewSet):
    queryset = Attend.objects.select_related("track", "user")
    serializer_classes = {
        "list": AttendSerializer,
        "create": AttendCreateSerializer,
        "retrieve": AttendDetailSerializer,
        "update": AttendUpdateSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.none()
