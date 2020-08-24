from unittest.mock import patch

from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase

from members.models import User


class AuthTokenAPITest(APITestCase):
    URL = "/v1/auth/token/"

    def test_auth_token_type_email(self):
        email = "sample@sample.com"
        password = "sample_password"
        User.objects.create_user(
            type="email", email=email, password=password,
        )
        response = self.client.post(
            self.URL, data={"email": email, "password": password,}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EmailVerificationAPITest(APITestCase):
    URL = "/v1/auth/email-verification/"

    def test_create(self):
        email = "sample@sample.com"
        response = self.client.post(self.URL, data={"email": email}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(mail.outbox[0].subject, "let us: Go! 이메일 인증 코드")

    def test_create_failed(self):
        with patch("members.apis.send_mail", return_value=0):
            email = "sample@sample.com"
            response = self.client.post(self.URL, data={"email": email}, format="json")
            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            self.assertEqual(len(mail.outbox), 0)

    def test_multi_create(self):
        email = "sample@sample.com"
        response1 = self.client.post(self.URL, data={"email": email}, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        response2 = self.client.post(self.URL, data={"email": email}, format="json")
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
