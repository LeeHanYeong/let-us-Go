from rest_framework import serializers

from sponsors.serializers import SponsorTierDetailSerializer
from ..models import (
    Seminar,
    Session,
    Speaker,
    Track,
    SessionLink,
    SessionFile,
    SessionVideo,
    SpeakerLink,
    SpeakerLinkType,
)

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

    'link_set',
)


class SessionVideoSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display')

    class Meta:
        model = SessionVideo
        fields = (
            'type',
            'type_display',
            'name',
            'key',
            'url',
        )


class SessionLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionLink
        fields = (
            'name',
            'url',
        )


class SessionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionFile
        fields = (
            'name',
            'attachment',
        )


class SpeakerLinkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeakerLinkType
        fields = (
            'pk',
            'name',
            'img_icon',
        )


class SpeakerLinkSerializer(serializers.ModelSerializer):
    type = SpeakerLinkTypeSerializer()

    class Meta:
        model = SpeakerLink
        fields = (
            'pk',
            'type',
            'name',
            'url',
        )


class SpeakerSerializer(serializers.ModelSerializer):
    link_set = SpeakerLinkSerializer(many=True)

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
    video_set = SessionVideoSerializer(many=True)
    link_set = SessionLinkSerializer(many=True)
    file_set = SessionFileSerializer(many=True)

    class Meta:
        model = Session
        fields = SESSION_FIELDS + (
            'video_set',
            'link_set',
            'file_set',
        )


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
    sponsor_tier_set = SponsorTierDetailSerializer(many=True)

    class Meta:
        model = Seminar
        fields = SEMINAR_FIELDS + (
            'track_set',
            'sponsor_tier_set',
        )
