from django.urls import path

from . import apis

urlpatterns = [
    path('', apis.AttendListCreateAPIView.as_view()),
    path('<int:pk>/', apis.AttendRetrieveUpdateAPIView.as_view()),
]
