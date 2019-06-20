from rest_framework import serializers

from members.serializers import UserSerializer
from ..models import Seminar, Session


class SeminarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seminar
        fields = (
            'pk',
            'name',
            'start_at',
            'end_at',
            'address1',
            'address2',
            'entry_fee',
            'after_party_fee',
        )


class SessionSerializer(serializers.ModelSerializer):
    speaker = UserSerializer()

    class Meta:
        model = Session
        fields = (
            'pk',
            'level',
            'name',
            'short_description',
            'description',
            'speaker_alt_text',
            'start_time',
            'end_time',

            'speaker',
        )


class SeminarDetailSerializer(serializers.ModelSerializer):
    session_set = SessionSerializer(many=True)

    class Meta:
        model = Seminar
        fields = (
            'pk',
            'name',
            'start_at',
            'end_at',
            'address1',
            'address2',
            'entry_fee',
            'after_party_fee',

            'session_set',
        )


class SessionDetailSerializer(serializers.ModelSerializer):
    speaker = UserSerializer()

    class Meta:
        model = Session
        fields = (
            'pk',
            'level',
            'name',
            'short_description',
            'description',
            'speaker_alt_text',
            'start_time',
            'end_time',

            'speaker',
        )
