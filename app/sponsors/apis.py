from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from utils.drf.exceptions import ValidationError
from .filters import SponsorTierFilterSet
from .models import SponsorTier
from .serializers import SponsorTierDetailSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='SponsorTier List',
        operation_description='스폰서 등급(List), 스폰서 목록 포함'
    )
)
class SponsorTierListAPIView(generics.ListAPIView):
    queryset = SponsorTier.objects.all()
    serializer_class = SponsorTierDetailSerializer
    filterset_class = SponsorTierFilterSet

    def get_queryset(self):
        if not self.kwargs.get('seminar'):
            raise ValidationError('seminar항목은 필수입니다')
        return super().get_queryset()