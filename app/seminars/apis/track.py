from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from ..models import Track
from ..serializers import TrackSerializer, TrackDetailSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Track List',
        operation_description='트랙(List)'
    )
)
class TrackListAPIView(generics.ListAPIView):
    Track.objects.all()
    serializer_class = TrackSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Track Detail',
        operation_description='트랙(Retrieve)'
    )
)
class TrackRetrieveAPIView(generics.RetrieveAPIView):
    Track.objects.all()
    serializer_class = TrackDetailSerializer
