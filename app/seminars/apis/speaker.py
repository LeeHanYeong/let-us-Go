from django_aid.drf.viewsets import ListModelViewSet

from ..filters import SpeakerFilterSet
from ..models import Speaker
from ..serializers import SpeakerSerializer

__all__ = ("SpeakerViewSet",)


class SpeakerViewSet(ListModelViewSet):
    queryset = Speaker.objects.annotate_choices()
    serializer_class = SpeakerSerializer
    filterset_class = SpeakerFilterSet
