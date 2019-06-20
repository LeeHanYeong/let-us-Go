from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from ..models import Seminar
from ..serializers import SeminarDetailSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Seminar List',
        operation_description='전체 세미나 목록'
    )
)
class SessionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Seminar.objects.all()
    serializer_class = SeminarDetailSerializer
