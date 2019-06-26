from django.urls import path

from . import apis

app_name = 'members'
urlpatterns = [
    path('', apis.UserCreateAPIView.as_view()),
    path('<int:pk>/', apis.UserRetrieveUpdateDestroyAPIView.as_view()),
    path('available/', apis.UserAttributeAvailableAPIView.as_view()),
]
