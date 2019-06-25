from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from members.serializers import UserSerializer
from seminars.serializers import SeminarSerializer
from .models import Attend


class AttendSerializer(serializers.ModelSerializer):
    seminar = SeminarSerializer()
    user = UserSerializer()

    class Meta:
        model = Attend
        fields = (
            'pk',
            'is_canceled',
            'seminar',
            'status',
            'user',
            'name',
            'type',
            'is_attend_after_party',
        )


class AttendCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attend
        fields = (
            'seminar',
            'name',
            'type',
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


class AttendDetailSerializer(serializers.ModelSerializer):
    seminar = SeminarSerializer()
    user = UserSerializer()

    class Meta:
        model = Attend
        fields = (
            'pk',
            'seminar',
            'is_canceled',
            'user',
            'name',
            'type',
            'is_attend_after_party',
        )


class AttendUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attend
        fields = (
            'is_canceled',
            'name',
            'is_attend_after_party',
        )
