from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from ..filters import SeminarFilterSet
from ..models import Seminar
from ..serializers import SeminarSerializer, SeminarDetailSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Seminar List',
        operation_description='세미나(List)'
    )
)
class SeminarListAPIView(generics.ListAPIView):
    queryset = Seminar.objects.all()
    serializer_class = SeminarSerializer
    filterset_class = SeminarFilterSet


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Seminar Detail',
        operation_description='세미나(Retrieve)<br>id에 0보내면 가장 최근 세미나를 리턴',
    )
)
class SeminarRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Seminar.objects.prefetch_related(
        'track_set__session_set__file_set',
        'track_set__session_set__video_set',
        'track_set__session_set__link_set',
        'track_set__session_set__speaker',
        'track_set__session_set__speaker__link_set',
        'sponsor_tier_set__sponsor_set',
    )
    serializer_class = SeminarDetailSerializer

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if self.kwargs.get(lookup_url_kwarg) == 0:
            return self.queryset.first()
        return super().get_object()
