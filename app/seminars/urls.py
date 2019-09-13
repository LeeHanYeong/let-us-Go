from django.urls import path

from . import apis

app_name = 'seminars'
urlpatterns = [
    path('', apis.SeminarListAPIView.as_view()),
    path('<int:pk>/', apis.SeminarRetrieveAPIView.as_view()),
    path('search/', apis.SessionSearchAPIView.as_view()),

    path('tracks/', apis.TrackListAPIView.as_view()),
    path('tracks/<int:pk>/', apis.TrackRetrieveAPIView.as_view()),

    path('sessions/', apis.SessionListAPIView.as_view()),
    path('sessions/<int:pk>/', apis.SessionRetrieveAPIView.as_view()),

    path('speakers/', apis.SpeakerListAPIView.as_view()),
]
