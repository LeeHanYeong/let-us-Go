# Auth
AUTH_USER_MODEL = "members.User"
AUTHENTICATION_BACKENDS = [
    "rest_framework_social_oauth2.backends.DjangoOAuth2",
    "django.contrib.auth.backends.ModelBackend",
    "members.backends.SettingsBackend",
]
DRFSO2_PROPRIETARY_BACKEND_NAME = "letusgo"
# DRFSO2_URL_NAMESPACE = 'oauth'
DEFAULT_USERS = {
    "dev@lhy.kr": {
        "password": "pbkdf2_sha256$150000$89oDFBSARLc8$Jsv1BlODbmILIiENOq3/2cvQM4663zW+clxzm52Fo28=",
        "name": "이한영",
        "type": "email",
        "phone_number": "010-4432-1234",
        "is_staff": True,
        "is_superuser": True,
    },
}
