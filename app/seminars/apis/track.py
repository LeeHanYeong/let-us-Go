from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from ..models import Track
from ..serializers import TrackSerializer, TrackDetailSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Track List", operation_description="트랙(List)"
    ),
)
class TrackListAPIView(generics.ListAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Track Detail", operation_description="트랙(Retrieve)"
    ),
)
class TrackRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Track.objects.prefetch_related(
        "session_set__file_set",
        "session_set__link_set",
        "session_set__video_set",
        "session_set__speaker",
        "session_set__speaker__link_set",
    )
    serializer_class = TrackDetailSerializer
