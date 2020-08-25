from copy import deepcopy

from django.test import TestCase
from model_bakery import baker
from rest_framework.exceptions import ValidationError

from members.models import EmailVerification, User
from members.serializers import UserCreateSerializer, EmailVerificationCreateSerializer


class UserCreateSerializerTest(TestCase):
    def test_validate(self):
        email = "sample@sample.com"
        ev = baker.make(EmailVerification, email=email)
        data = {
            "type": "email",
            "email": email,
            "password1": "password1",
            "password2": "password2",
            "email_verification_code": ev.code,
        }

        # password1, password2
        with self.assertRaises(ValidationError) as cm:
            serializer = UserCreateSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        exception = cm.exception
        self.assertEqual(exception.detail["password2"][0].code, "invalid")

        # email_verification_code | invalid
        with self.assertRaises(ValidationError) as cm:
            data = deepcopy(data)
            data["email_verification_code"] += "a"
            data["password2"] = "password1"
            serializer = UserCreateSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        exception = cm.exception
        self.assertEqual(
            exception.detail["email_verification_code"][0].code,
            "email_verification_code_invalid",
        )

        # email_verification_code | does not exist
        ev.delete()
        with self.assertRaises(ValidationError) as cm:
            data = deepcopy(data)
            data["password2"] = "password1"
            serializer = UserCreateSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        exception = cm.exception
        self.assertEqual(
            exception.detail["email_verification_code"][0].code,
            "email_verification_does_not_exist",
        )


class EmailVerificationCreateSerializerTest(TestCase):
    def test_validate(self):
        email = "sample@sample.com"
        baker.make(User, email=email)

        data = {"email": email}
        with self.assertRaises(ValidationError) as cm:
            serializer = EmailVerificationCreateSerializer(data=data)
            serializer.is_valid(raise_exception=True)

        exception = cm.exception
        self.assertEqual(exception.detail["email"][0].code, "invalid")
