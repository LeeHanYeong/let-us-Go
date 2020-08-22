from django_aid.drf.viewsets import ReadOnlyModelViewSet

from ..models import Track
from ..serializers import TrackSerializer, TrackDetailSerializer

__all__ = ("TrackViewSet",)


class TrackViewSet(ReadOnlyModelViewSet):
    queryset = Track.objects.annotate_choices()
    serializer_classes = {
        "list": TrackSerializer,
        "retrieve": TrackDetailSerializer,
    }

    def get_queryset(self):
        if self.action == "retrieve":
            return self.queryset.prefetch_related(
                "session_set__file_set",
                "session_set__link_set",
                "session_set__video_set",
                "session_set__speaker",
                "session_set__speaker__link_set",
            )
        return self.queryset
