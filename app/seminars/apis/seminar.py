from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

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


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_summary='Seminar Detail',
        operation_description='세미나(Retrieve)'
    )
)
class SeminarRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Seminar.objects.all()
    serializer_class = SeminarDetailSerializer
