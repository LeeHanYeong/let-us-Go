from django.utils.decorators import method_decorator
from drf_yasg.openapi import Parameter, IN_PATH
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Session
from ..serializers import SessionDetailSerializer, SessionSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Session List',
        operation_description='세션(List)'
    )
)
class SessionListAPIView(generics.ListAPIView):
    queryset = Session.objects.select_related(
        'speaker',
    ).prefetch_related(
        'speaker__link_set',
    )
    serializer_class = SessionSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Session Detail',
        operation_description='세션(Retrieve)'
    )
)
class SessionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionDetailSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Session Search',
        operation_description='세션 검색(Search)',
        manual_parameters=[
            Parameter('keyword', IN_PATH, type='string'),
        ]
    )
)
class SessionSearchAPIView(APIView):
    def get(self, request):
        keyword = request.query_params.get('keyword', '')
        if len(keyword) < 3:
            raise ValidationError('검색어는 최소 3글자 이상이어야 합니다')
        sessions = Session.objects.filter(name__icontains=keyword)
        count = sessions.count()
        if count > 100:
            sessions = sessions[:100]

        search_result_dict = {}
        for session in sessions:
            search_result_dict.setdefault(session.track.seminar.name, [])
            search_result_dict[session.track.seminar.name].append(
                SessionSerializer(session).data,
            )
        return Response(search_result_dict)
