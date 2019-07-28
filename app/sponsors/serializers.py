from rest_framework import serializers

from .models import Sponsor, SponsorTier

SPONSOR_TIER_FIELDS = (
    'pk',
    'name',
)
SPONSOR_FIELDS = (
    'pk',
    'name',
    'logo',
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
        fields = SPONSOR_TIER_FIELDS + (
            'sponsor_set',
        )
