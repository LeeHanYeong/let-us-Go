from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()

__all__ = (
    'SettingsBackend',
)


class SettingsBackend:
    def authenticate(self, request, email=None, password=None):
        email_valid = email in settings.DEFAULT_USERS.keys()
        user_dict = settings.DEFAULT_USERS.get(email, {})

        password_valid = check_password(password, user_dict.get('password', ''))
        if email_valid and password_valid:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User(email=email, **user_dict)
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
