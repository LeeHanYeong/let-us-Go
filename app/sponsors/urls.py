from django.urls import path

from . import apis

app_name = 'sponsors'
urlpatterns = [
    path('tiers/', apis.SponsorTierListAPIView.as_view()),
]
