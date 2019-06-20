from django.urls import path

from . import apis

app_name = 'seminars'
urlpatterns = [
    path('', apis.SeminarListAPIView.as_view()),
    path('<int:pk>/', apis.SeminarRetrieveAPIView.as_view()),
]
