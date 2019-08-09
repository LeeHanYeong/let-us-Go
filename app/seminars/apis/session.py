from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

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
