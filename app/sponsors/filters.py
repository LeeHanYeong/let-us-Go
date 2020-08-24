from django_filters import rest_framework as filters

from .models import SponsorTier


class SponsorTierFilterSet(filters.FilterSet):
    seminar = filters.CharFilter(required=True)

    class Meta:
        model = SponsorTier
        fields = ("seminar",)
