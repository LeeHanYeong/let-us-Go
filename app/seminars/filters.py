from django_filters import rest_framework as filters
from rest_framework.generics import get_object_or_404

from .models import Seminar, Speaker


class SeminarFilterSet(filters.FilterSet):
    class Meta:
        model = Seminar
        fields = ("year",)


class SpeakerFilterSet(filters.FilterSet):
    seminar = filters.CharFilter(help_text="Seminar의 pk(id)", method="seminar_filter")

    class Meta:
        model = Speaker
        fields = ("seminar",)

    def seminar_filter(self, queryset, name, value):
        seminar = get_object_or_404(Seminar, pk=value)
        return queryset.filter(session_set__track__seminar=seminar)
