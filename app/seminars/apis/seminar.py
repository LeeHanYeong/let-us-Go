from django_aid.drf.viewsets import ReadOnlyModelViewSet

from ..filters import SeminarFilterSet
from ..models import Seminar
from ..serializers import SeminarSerializer, SeminarDetailSerializer

__all__ = ("SeminarViewSet",)


class SeminarViewSet(ReadOnlyModelViewSet):
    queryset = Seminar.objects.annotate_choices()
    serializer_class = {
        "list": SeminarSerializer,
        "retrieve": SeminarDetailSerializer,
    }
    filterset_class = SeminarFilterSet

    def get_queryset(self):
        if self.action == "retrieve":
            return self.queryset.prefetch_related(
                "track_set__session_set__file_set",
                "track_set__session_set__video_set",
                "track_set__session_set__link_set",
                "track_set__session_set__speaker",
                "track_set__session_set__speaker__link_set",
                "sponsor_tier_set__sponsor_set",
            )
        return self.queryset

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if self.kwargs.get(lookup_url_kwarg) == 0:
            return self.queryset.first()
        return super().get_object()
