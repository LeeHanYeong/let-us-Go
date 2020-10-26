from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()

__all__ = ("SettingsBackend",)


class SettingsBackend:
    def authenticate(self, request, username=None, password=None):
        email_valid = username in settings.DEFAULT_USERS.keys()
        user_dict = settings.DEFAULT_USERS.get(username, {})

        password_valid = check_password(password, user_dict.get("password", ""))
        if email_valid and password_valid:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                user = User.objects.update_or_create(
                    email=username,
                    defaults={
                        "username": username,
                        **user_dict,
                    },
                )[0]
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class SocialBackend:
    def authenticate(self, request, type, uid):
        try:
            return User.objects.get(type=type, username=uid)
        except User.DoesNotExist:
            return
