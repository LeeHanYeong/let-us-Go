from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from members.serializers import UserSerializer
from seminars.serializers import TrackDetailSerializer
from .models import Attend

ATTEND_FIELDS = (
    'id',
    'is_canceled',
    'track',
    'status',
    'name',

    'applicant_type',
    'applicant_type_display',
    'discount_type',
    'discount_type_display',

    'is_attend_after_party',
)


class AttendSerializer(serializers.ModelSerializer):
    track = TrackDetailSerializer()
    applicant_type_display = serializers.CharField(
        source='get_applicant_type_display', help_text='지원자 구분의 display name')
    discount_type_display = serializers.CharField(
        source='get_discount_type_display', help_text='할인 구분의 display name')

    class Meta:
        model = Attend
        fields = ATTEND_FIELDS


class AttendCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Attend
        fields = (
            'track',
            'user',
            'name',
            'applicant_type',
            'discount_type',
            'is_attend_after_party',
        )

    def validate_track(self, value):
        return value

    def validate_user(self, value):
        return value

    def validate(self, attrs):
        user = attrs['user']
        track = attrs['track']
        if Attend.objects.filter(user=user, track=track).exists():
            raise ValidationError('이미 신청내역이 있습니다')
        return attrs

    def to_representation(self, instance):
        return AttendDetailSerializer(instance).data


class AttendDetailSerializer(AttendSerializer):
    user = UserSerializer()

    class Meta:
        model = Attend
        fields = ATTEND_FIELDS + (
            'user',
        )


class AttendUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attend
        fields = (
            'is_canceled',
            'name',
            'is_attend_after_party',
        )
