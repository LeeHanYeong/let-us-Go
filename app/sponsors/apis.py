from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .filters import SponsorTierFilterSet
from .models import SponsorTier
from .serializers import SponsorTierDetailSerializer

__all__ = ("SponsorTierListAPIView",)


class SponsorTierListAPIView(generics.ListAPIView):
    queryset = SponsorTier.objects.prefetch_related("sponsor_set",)
    serializer_class = SponsorTierDetailSerializer
    filterset_class = SponsorTierFilterSet

    def get_queryset(self):
        if not self.request.query_params.get("seminar"):
            raise ValidationError("seminar항목은 필수입니다")
        return self.queryset
