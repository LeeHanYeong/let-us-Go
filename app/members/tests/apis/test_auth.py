from unittest.mock import patch

from django.core import mail
from django.utils.crypto import get_random_string
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from members.models import User, EmailVerification


class AuthTokenAPITest(APITestCase):
    URL_EMAIL = "/v1/auth/token/"
    URL_SOCIAL = "/v1/auth/token/social/"

    def test_auth_token_type_email(self):
        email = "sample@sample.com"
        password = "sample_password"
        User.objects.create_user(
            type="email",
            email=email,
            password=password,
        )
        response = self.client.post(
            self.URL_EMAIL,
            data={
                "email": email,
                "password": password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_token_type_email_failed(self):
        email = "sample@sample.com"
        password = "sample_password"
        User.objects.create_user(
            type="email",
            email=email,
            password=password,
        )
        response = self.client.post(
            self.URL_EMAIL,
            data={
                "email": "a" + email,
                "password": password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auth_token_type_social(self):
        type = User.TYPE_APPLE
        email = "sample@sample.com"
        uid = get_random_string(length=20)
        User.objects.create_user(
            type=type,
            email=email,
            uid=uid,
        )
        response = self.client.post(self.URL_SOCIAL, data={"type": type, "uid": uid})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_token_type_social_failed(self):
        type = User.TYPE_APPLE
        email = "sample@sample.com"
        uid = get_random_string(length=20)
        User.objects.create_user(
            type=type,
            email=email,
            uid=uid + "1",
        )
        response = self.client.post(self.URL_SOCIAL, data={"type": type, "uid": uid})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EmailVerificationAPITest(APITestCase):
    URL = "/v1/auth/email-verification/"
    URL_CHECK = "/v1/auth/email-verification/check/"

    def test_create(self):
        email = "sample@sample.com"
        response = self.client.post(self.URL, data={"email": email}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(mail.outbox[0].subject, "let us: Go! 이메일 인증 코드 안내")

    def test_create_failed(self):
        with patch("members.models.send_mail", return_value=0):
            email = "sample@sample.com"
            response = self.client.post(self.URL, data={"email": email}, format="json")
            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            self.assertEqual(len(mail.outbox), 0)

    def test_create_type_signup_failed_when_user_email_exists(self):
        email = "sample@sample.com"
        baker.make(User, email=email)
        response = self.client.post(self.URL, data={"email": email})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]["message"], f"해당 이메일({email})은 이미 사용중입니다")

    def test_multi_create_only_remain_one(self):
        email = "sample@sample.com"
        response1 = self.client.post(self.URL, data={"email": email}, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        response2 = self.client.post(self.URL, data={"email": email}, format="json")
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmailVerification.objects.filter(email=email).count(), 1)

    def test_check(self):
        email = "sample@sample.com"
        ev = baker.make(EmailVerification, email=email)
        response = self.client.post(
            self.URL_CHECK,
            data={
                "email": email,
                "code": ev.code,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.post(
            self.URL_CHECK,
            data={
                "email": "another@sample.com",
                "code": ev.code,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(
            self.URL_CHECK,
            data={
                "email": email,
                "code": ev.code + "a",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
