from django.urls import path

from . import apis

members_patterns = (
    [
        path("", apis.UserCreateAPIView.as_view()),
        path("<int:pk>/", apis.UserRetrieveUpdateDestroyAPIView.as_view()),
        path("profile/", apis.UserProfileAPIView.as_view()),
        path("available/", apis.UserAttributeAvailableAPIView.as_view()),
    ],
    "members",
)
auth_patterns = (
    [
        path("token/", apis.AuthTokenAPIView.as_view()),
        path("email-verification/", apis.EmailVerificationCreateAPIView.as_view()),
    ],
    "auth",
)
