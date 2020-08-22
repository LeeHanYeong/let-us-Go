from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from ..filters import SpeakerFilterSet
from ..models import Speaker
from ..serializers import SpeakerSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Speaker List", operation_description="발표자 목록"
    ),
)
class SpeakerListAPIView(generics.ListAPIView):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    filterset_class = SpeakerFilterSet
