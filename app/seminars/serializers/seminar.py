from rest_framework import serializers

from ..models import Seminar, Session, Speaker, Track

SEMINAR_FIELDS = (
    'pk',
    'name',
    'start_at',
    'end_at',
    'address1',
    'address2',
    'after_party_fee',
    'img_sponsors_web',
    'img_sponsors_mobile',
)
TRACK_FIELDS = (
    'pk',
    'name',
    'location',
    'total_attend_count',
    'attend_count',
    'entry_fee',
    'entry_fee_student',
)
SESSION_FIELDS = (
    'pk',
    'level',
    'level_display',
    'name',
    'short_description',
    'description',
    'speaker_alt_text',
    'start_time',
    'end_time',

    'speaker',
)
SPEAKER_FIELDS = (
    'pk',
    'name',
    'email',
    'phone_number',
    'img_profile',
    'facebook',
    'github',
)


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = SPEAKER_FIELDS


class SeminarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seminar
        fields = SEMINAR_FIELDS


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = TRACK_FIELDS


class SessionSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(source='get_level_display')
    speaker = SpeakerSerializer()

    class Meta:
        model = Session
        fields = SESSION_FIELDS


class SessionDetailSerializer(SessionSerializer):
    pass


class TrackDetailSerializer(serializers.ModelSerializer):
    seminar = SeminarSerializer()
    session_set = SessionDetailSerializer(many=True)

    class Meta:
        model = Track
        fields = TRACK_FIELDS + (
            'seminar',
            'session_set',
        )


class SeminarDetailSerializer(serializers.ModelSerializer):
    track_set = TrackDetailSerializer(many=True)

    class Meta:
        model = Seminar
        fields = SEMINAR_FIELDS + (
            'track_set',
        )
