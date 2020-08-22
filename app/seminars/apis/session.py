from django.db.models import F
from django_aid.drf.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ..models import Session, Seminar
from ..serializers import SessionDetailSerializer, SessionSerializer, SeminarSerializer

__all__ = ("SessionViewSet",)


class SessionViewSet(ReadOnlyModelViewSet):
    queryset = (
        Session.objects.annotate_choices()
        .select_related("speaker",)
        .prefetch_related("speaker__link_set",)
    )
    serializer_classes = {
        "list": SessionSerializer,
        "retrieve": SessionDetailSerializer,
    }

    @action(detail=False, methods=["get"])
    def search(self, request, *args, **kwargs):
        keyword = request.query_params.get("keyword", "")
        if len(keyword) < 2:
            raise ValidationError("검색어는 최소 2글자 이상이어야 합니다")

        sessions = (
            Session.objects.prefetch_related("link_set", "file_set", "video_set",)
            .filter(name__icontains=keyword,)
            .annotate(seminar=F("track__seminar"),)
        )

        seminars = Seminar.objects.filter(track_set__session_set__in=sessions,)

        search_results = []
        for seminar in seminars:
            seminar_sessions = [
                session for session in sessions if session.seminar == seminar.id
            ]
            result_dict = {
                "seminar": SeminarSerializer(seminar).data,
                "sessions": SessionDetailSerializer(seminar_sessions, many=True).data,
            }
            search_results.append(result_dict)

        return Response(search_results)
