from django.test import TestCase
from rest_framework.exceptions import ValidationError

from members.models import User


class UserManagerTest(TestCase):
    def test_create_user_type_email(self):
        email = "sample@sample.com"
        user = User.objects.create_user(email=email, type="email")
        self.assertEqual(user.username, email)

    def test_create_user_require_username(self):
        email = "sample@sample.com"
        with self.assertRaises(ValidationError):
            User.objects.create_user(email=email)
