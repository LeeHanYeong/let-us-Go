from rest_framework import serializers

from .models import Sponsor, SponsorTier

SPONSOR_TIER_FIELDS = (
    "id",
    "name",
)
SPONSOR_FIELDS = (
    "id",
    "name",
    "logo",
    "logo_white",
    "logo_white_bgcolor",
)


class SponsorTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorTier
        fields = SPONSOR_TIER_FIELDS


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = SPONSOR_FIELDS


class SponsorTierDetailSerializer(serializers.ModelSerializer):
    sponsor_set = SponsorSerializer(many=True)

    class Meta:
        model = SponsorTier
        fields = SPONSOR_TIER_FIELDS + ("sponsor_set",)
