from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from members.serializers import UserSerializer
from seminars.serializers import TrackDetailSerializer
from .models import Attend

ATTEND_FIELDS = (
    'pk',
    'is_canceled',
    'track',
    'status',
    'user',
    'name',

    'applicant_type',
    'applicant_type_display',
    'discount_type',
    'discount_type_display',

    'is_attend_after_party',
)


class AttendSerializer(serializers.ModelSerializer):
    track = TrackDetailSerializer()
    user = UserSerializer()

    applicant_type_display = serializers.CharField(
        source='get_applicant_type_display', help_text='지원자 구분의 display name')
    discount_type_display = serializers.CharField(
        source='get_discount_type_display', help_text='할인 구분의 display name')

    class Meta:
        model = Attend
        fields = ATTEND_FIELDS


class AttendCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attend
        fields = (
            'track',
            'name',
            'applicant_type',
            'discount_type',
            'is_attend_after_party',
        )

    def create(self, validated_data):
        user = validated_data['user']
        seminar = validated_data['seminar']
        if Attend.objects.filter(user=user, seminar=seminar).exists():
            raise ValidationError('이미 신청내역이 있습니다')
        super().create(validated_data)

    def to_representation(self, instance):
        return AttendDetailSerializer(instance).data


class AttendDetailSerializer(AttendSerializer):
    class Meta:
        model = Attend
        fields = ATTEND_FIELDS


class AttendUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attend
        fields = (
            'is_canceled',
            'name',
            'is_attend_after_party',
        )
