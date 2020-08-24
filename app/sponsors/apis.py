from rest_framework import generics

from .filters import SponsorTierFilterSet
from .models import SponsorTier
from .serializers import SponsorTierDetailSerializer

__all__ = ("SponsorTierListAPIView",)


class SponsorTierListAPIView(generics.ListAPIView):
    queryset = SponsorTier.objects.prefetch_related("sponsor_set",)
    serializer_class = SponsorTierDetailSerializer
    filterset_class = SponsorTierFilterSet
