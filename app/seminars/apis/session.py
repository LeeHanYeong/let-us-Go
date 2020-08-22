from django.db.models import F
from django.utils.decorators import method_decorator
from drf_yasg.openapi import Parameter, IN_PATH
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Session, Seminar
from ..serializers import SessionDetailSerializer, SessionSerializer, SeminarSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Session List", operation_description="세션(List)"
    ),
)
class SessionListAPIView(generics.ListAPIView):
    queryset = Session.objects.select_related("speaker",).prefetch_related(
        "speaker__link_set",
    )
    serializer_class = SessionSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Session Detail", operation_description="세션(Retrieve)"
    ),
)
class SessionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionDetailSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Session Search",
        operation_description="세션 검색(Search)",
        manual_parameters=[Parameter("keyword", IN_PATH, type="string"),],
    ),
)
class SessionSearchAPIView(APIView):
    def get(self, request):
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
